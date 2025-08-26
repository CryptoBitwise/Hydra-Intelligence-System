from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from backend.core.database import get_db, IntelligenceModel
from backend.api.models import Intelligence, IntelligenceCreate, ThreatLevelEnum

router = APIRouter(
    prefix="/api/intelligence",
    tags=["intelligence"]
)

@router.get("/trends")
async def get_intelligence_trends(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """Get intelligence trends over time"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    from sqlalchemy import func
    
    # Trends by threat level
    threat_trends = db.query(
        IntelligenceModel.threat_level,
        func.count(IntelligenceModel.id).label('count')
    ).filter(
        IntelligenceModel.timestamp >= start_date
    ).group_by(
        IntelligenceModel.threat_level
    ).all()
    
    # Trends by competitor
    competitor_trends = db.query(
        IntelligenceModel.competitor,
        func.count(IntelligenceModel.id).label('count')
    ).filter(
        IntelligenceModel.timestamp >= start_date
    ).group_by(
        IntelligenceModel.competitor
    ).order_by(
        func.count(IntelligenceModel.id).desc()
    ).limit(10).all()
    
    # Trends by head
    head_trends = db.query(
        IntelligenceModel.head,
        func.count(IntelligenceModel.id).label('count')
    ).filter(
        IntelligenceModel.timestamp >= start_date
    ).group_by(
        IntelligenceModel.head
    ).all()
    
    return {
        "period_days": days,
        "threat_levels": {level: count for level, count in threat_trends},
        "top_competitors": [{"competitor": comp, "discoveries": count} for comp, count in competitor_trends],
        "head_activity": {head: count for head, count in head_trends}
    }

@router.get("/search")
async def search_intelligence(
    q: str = Query(..., description="Search query"),
    db: Session = Depends(get_db)
):
    """Search intelligence by text"""
    
    # Search in discovery and recommended_action fields
    results = db.query(IntelligenceModel).filter(
        (IntelligenceModel.discovery.contains(q)) |
        (IntelligenceModel.recommended_action.contains(q))
    ).limit(50).all()
    
    return results
