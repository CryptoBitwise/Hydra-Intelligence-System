from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import asyncio
import json

from backend.core.database import get_db, IntelligenceModel, CompetitorModel, HeadStatusModel, AlertModel
from backend.api.models import (
    Intelligence, IntelligenceCreate,
    Competitor, CompetitorCreate,
    HeadStatus, DashboardStats,
    WebSocketMessage, HeadConfig,
    AlertConfig, BulkIntelligenceQuery,
    ThreatLevelEnum
)
from backend.api.routers.intelligence import router as intelligence_router
from backend.api.routers.integrations import router as integrations_router

app = FastAPI(
    title="HYDRA Intelligence API",
    description="6-headed competitive intelligence system",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(intelligence_router)
app.include_router(integrations_router)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        await self.send_personal_message(
            {"type": "connection", "message": "Connected to HYDRA"},
            websocket
        )
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except:
                # Handle broken connections
                try:
                    self.disconnect(connection)
                except:
                    pass

manager = ConnectionManager()

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "HYDRA Intelligence System",
        "status": "operational",
        "heads": ["PriceWatch", "JobSpy", "TechRadar", "SocialPulse", "PatentHawk", "AdTracker"],
        "version": "1.0.0"
    }

# Intelligence endpoints
@app.post("/api/intelligence", response_model=Intelligence)
async def create_intelligence(
    intelligence: IntelligenceCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create new intelligence entry and broadcast to connected clients"""
    
    # Save to database
    db_intel = IntelligenceModel(**intelligence.dict())
    db.add(db_intel)
    db.commit()
    db.refresh(db_intel)
    
    # Broadcast to WebSocket clients
    await manager.broadcast({
        "type": "intelligence",
        "data": {
            "id": db_intel.id,
            "head": db_intel.head,
            "competitor": db_intel.competitor,
            "discovery": db_intel.discovery,
            "threat_level": db_intel.threat_level,
            "confidence": db_intel.confidence,
            "timestamp": db_intel.timestamp.isoformat() if db_intel.timestamp else datetime.utcnow().isoformat(),
            "recommended_action": db_intel.recommended_action
        }
    })
    
    # Trigger alerts for high/critical threats
    if db_intel.threat_level in [ThreatLevelEnum.high, ThreatLevelEnum.critical]:
        background_tasks.add_task(send_alerts, db_intel)
    
    return db_intel

@app.get("/api/intelligence", response_model=List[Intelligence])
async def get_intelligence(
    skip: int = 0,
    limit: int = 100,
    competitor: Optional[str] = None,
    head: Optional[str] = None,
    threat_level: Optional[ThreatLevelEnum] = None,
    db: Session = Depends(get_db)
):
    """Get intelligence with filters"""
    
    query = db.query(IntelligenceModel)
    
    if competitor:
        query = query.filter(IntelligenceModel.competitor == competitor)
    if head:
        query = query.filter(IntelligenceModel.head == head)
    if threat_level:
        query = query.filter(IntelligenceModel.threat_level == threat_level)
    
    intelligence = query.order_by(IntelligenceModel.timestamp.desc()).offset(skip).limit(limit).all()
    return intelligence

@app.get("/api/intelligence/{intelligence_id}", response_model=Intelligence)
async def get_intelligence_by_id(
    intelligence_id: int,
    db: Session = Depends(get_db)
):
    """Get specific intelligence by ID"""
    
    intel = db.query(IntelligenceModel).filter(IntelligenceModel.id == intelligence_id).first()
    if not intel:
        raise HTTPException(status_code=404, detail="Intelligence not found")
    return intel

@app.patch("/api/intelligence/{intelligence_id}/status")
async def update_intelligence_status(
    intelligence_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update intelligence status (acknowledged, acted_upon, etc.)"""
    
    intel = db.query(IntelligenceModel).filter(IntelligenceModel.id == intelligence_id).first()
    if not intel:
        raise HTTPException(status_code=404, detail="Intelligence not found")
    
    intel.status = status
    db.commit()
    
    return {"message": "Status updated", "new_status": status}

# Competitor endpoints
@app.post("/api/competitors", response_model=Competitor)
async def add_competitor(
    competitor: CompetitorCreate,
    db: Session = Depends(get_db)
):
    """Add a new competitor to monitor"""
    
    # Check if already exists
    existing = db.query(CompetitorModel).filter(CompetitorModel.domain == competitor.domain).first()
    if existing:
        raise HTTPException(status_code=400, detail="Competitor already exists")
    
    db_competitor = CompetitorModel(**competitor.dict())
    db.add(db_competitor)
    db.commit()
    db.refresh(db_competitor)
    
    # Broadcast update
    await manager.broadcast({
        "type": "competitor_added",
        "data": {"domain": db_competitor.domain, "name": db_competitor.company_name}
    })
    
    return db_competitor

@app.get("/api/competitors", response_model=List[Competitor])
async def get_competitors(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all monitored competitors"""
    
    query = db.query(CompetitorModel)
    if active_only:
        query = query.filter(CompetitorModel.active == 1)
    
    competitors = query.all()
    
    # Convert active field from int to bool for response
    for comp in competitors:
        comp.active = bool(comp.active)
    
    return competitors

@app.delete("/api/competitors/{competitor_id}")
async def remove_competitor(
    competitor_id: int,
    db: Session = Depends(get_db)
):
    """Remove a competitor (soft delete)"""
    
    competitor = db.query(CompetitorModel).filter(CompetitorModel.id == competitor_id).first()
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor not found")
    
    competitor.active = 0
    db.commit()
    
    return {"message": "Competitor deactivated"}

# Head status endpoints
@app.get("/api/heads", response_model=List[HeadStatus])
async def get_head_status(db: Session = Depends(get_db)):
    """Get status of all HYDRA heads"""
    
    heads = db.query(HeadStatusModel).all()
    
    # If no heads in DB, initialize them
    if not heads:
        head_names = ["PriceWatch", "JobSpy", "TechRadar", "SocialPulse", "PatentHawk", "AdTracker"]
        for name in head_names:
            head = HeadStatusModel(
                head_name=name,
                status="inactive",
                discoveries_count=0,
                error_count=0
            )
            db.add(head)
        db.commit()
        heads = db.query(HeadStatusModel).all()
    
    return heads

@app.post("/api/heads/{head_name}/status")
async def update_head_status(
    head_name: str,
    status: str,
    db: Session = Depends(get_db)
):
    """Update head status"""
    
    head = db.query(HeadStatusModel).filter(HeadStatusModel.head_name == head_name).first()
    
    if not head:
        head = HeadStatusModel(head_name=head_name, status=status)
        db.add(head)
    else:
        head.status = status
        head.last_run = datetime.utcnow()
    
    db.commit()
    
    # Broadcast status update
    await manager.broadcast({
        "type": "head_status",
        "data": {"head": head_name, "status": status}
    })
    
    return {"message": "Status updated"}

@app.post("/api/heads/{head_name}/config")
async def update_head_config(
    head_name: str,
    config: HeadConfig,
    db: Session = Depends(get_db)
):
    """Update head configuration"""
    
    head = db.query(HeadStatusModel).filter(HeadStatusModel.head_name == head_name).first()
    
    if not head:
        raise HTTPException(status_code=404, detail="Head not found")
    
    head.config = config.config
    db.commit()
    
    return {"message": "Configuration updated"}

# Dashboard endpoints
@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics"""
    
    # Total discoveries
    total_discoveries = db.query(IntelligenceModel).count()
    
    # Threat counts
    critical_threats = db.query(IntelligenceModel).filter(
        IntelligenceModel.threat_level == ThreatLevelEnum.critical
    ).count()
    
    high_threats = db.query(IntelligenceModel).filter(
        IntelligenceModel.threat_level == ThreatLevelEnum.high
    ).count()
    
    # Active competitors
    active_competitors = db.query(CompetitorModel).filter(
        CompetitorModel.active == 1
    ).count()
    
    # Active heads
    active_heads = db.query(HeadStatusModel).filter(
        HeadStatusModel.status == "active"
    ).count()
    
    # Last 24h discoveries
    yesterday = datetime.utcnow() - timedelta(days=1)
    last_24h = db.query(IntelligenceModel).filter(
        IntelligenceModel.timestamp >= yesterday
    ).count()
    
    # Top threat competitor
    from sqlalchemy import func
    top_threat = db.query(
        IntelligenceModel.competitor,
        func.count(IntelligenceModel.id).label('count')
    ).filter(
        IntelligenceModel.threat_level.in_([ThreatLevelEnum.high, ThreatLevelEnum.critical])
    ).group_by(
        IntelligenceModel.competitor
    ).order_by(
        func.count(IntelligenceModel.id).desc()
    ).first()
    
    return DashboardStats(
        total_discoveries=total_discoveries,
        critical_threats=critical_threats,
        high_threats=high_threats,
        active_competitors=active_competitors,
        active_heads=active_heads,
        last_24h_discoveries=last_24h,
        top_threat_competitor=top_threat[0] if top_threat else None
    )

@app.get("/api/dashboard/timeline")
async def get_timeline(
    hours: int = 24,
    db: Session = Depends(get_db)
):
    """Get intelligence timeline for charts"""
    
    start_time = datetime.utcnow() - timedelta(hours=hours)
    
    intelligence = db.query(IntelligenceModel).filter(
        IntelligenceModel.timestamp >= start_time
    ).order_by(IntelligenceModel.timestamp.desc()).all()
    
    # Group by hour for timeline
    from collections import defaultdict
    timeline = defaultdict(lambda: {"count": 0, "threats": []})
    
    for intel in intelligence:
        hour_key = intel.timestamp.strftime("%Y-%m-%d %H:00")
        timeline[hour_key]["count"] += 1
        if intel.threat_level in [ThreatLevelEnum.high, ThreatLevelEnum.critical]:
            timeline[hour_key]["threats"].append({
                "level": intel.threat_level,
                "competitor": intel.competitor
            })
    
    return dict(timeline)

# Alert endpoints
@app.post("/api/alerts/config")
async def configure_alerts(
    config: AlertConfig,
    db: Session = Depends(get_db)
):
    """Configure alert settings"""
    
    # Store alert configuration
    # In production, this would go to a config table
    
    return {"message": "Alert configuration saved"}

@app.get("/api/alerts/history")
async def get_alert_history(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get alert history"""
    
    alerts = db.query(AlertModel).order_by(
        AlertModel.sent_at.desc()
    ).limit(limit).all()
    
    return alerts

# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif message.get("type") == "subscribe":
                # Handle subscription to specific competitors or heads
                await websocket.send_json({
                    "type": "subscribed",
                    "data": message.get("data")
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Advanced query endpoint
@app.post("/api/intelligence/query")
async def query_intelligence(
    query: BulkIntelligenceQuery,
    db: Session = Depends(get_db)
):
    """Advanced intelligence query with multiple filters"""
    
    q = db.query(IntelligenceModel)
    
    if query.competitors:
        q = q.filter(IntelligenceModel.competitor.in_(query.competitors))
    
    if query.heads:
        q = q.filter(IntelligenceModel.head.in_(query.heads))
    
    if query.threat_levels:
        q = q.filter(IntelligenceModel.threat_level.in_(query.threat_levels))
    
    if query.start_date:
        q = q.filter(IntelligenceModel.timestamp >= query.start_date)
    
    if query.end_date:
        q = q.filter(IntelligenceModel.timestamp <= query.end_date)
    
    results = q.order_by(IntelligenceModel.timestamp.desc()).limit(query.limit).all()
    
    return results

# Export endpoint
@app.get("/api/export")
async def export_intelligence(
    format: str = "json",
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Export intelligence data"""
    
    query = db.query(IntelligenceModel)
    
    if start_date:
        query = query.filter(IntelligenceModel.timestamp >= start_date)
    if end_date:
        query = query.filter(IntelligenceModel.timestamp <= end_date)
    
    data = query.all()
    
    if format == "json":
        return [
            {
                "id": d.id,
                "head": d.head,
                "competitor": d.competitor,
                "discovery": d.discovery,
                "threat_level": d.threat_level,
                "confidence": d.confidence,
                "timestamp": d.timestamp.isoformat() if d.timestamp else None,
                "data": d.data,
                "recommended_action": d.recommended_action
            }
            for d in data
        ]
    
    # Add CSV export if needed
    return {"error": "Unsupported format"}

# Health check endpoint
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check for monitoring"""
    
    try:
        # Check database connection
        db.execute("SELECT 1")
        
        # Check heads status
        active_heads = db.query(HeadStatusModel).filter(
            HeadStatusModel.status == "active"
        ).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "active_heads": active_heads,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# Background task for sending alerts
async def send_alerts(intelligence: IntelligenceModel):
    """Send alerts for critical intelligence"""
    
    # In production, integrate with Slack, email, etc.
    print(f"🚨 ALERT: {intelligence.threat_level} threat from {intelligence.competitor}")
    print(f"Discovery: {intelligence.discovery}")
    print(f"Action: {intelligence.recommended_action}")
    
    # Log alert to database
    # Implement actual alert sending logic here

# Initialize the HYDRA system on startup
@app.on_event("startup")
async def startup_event():
    """Initialize HYDRA on API startup"""
    print("""
    ╔════════════════════════════════════════════════╗
    ║         HYDRA API SERVER STARTED               ║
    ║                                                ║
    ║  Endpoints ready at:                           ║
    ║  http://localhost:8000                         ║
    ║                                                ║
    ║  WebSocket at:                                 ║
    ║  ws://localhost:8000/ws                        ║
    ║                                                ║
    ║  Documentation at:                             ║
    ║  http://localhost:8000/docs                    ║
    ╚════════════════════════════════════════════════╝
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
