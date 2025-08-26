from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ThreatLevelEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class IntelligenceBase(BaseModel):
    head: str
    competitor: str
    discovery: str
    threat_level: ThreatLevelEnum
    confidence: float = Field(ge=0, le=1)
    data: Dict[str, Any]
    recommended_action: str

class IntelligenceCreate(IntelligenceBase):
    pass

class Intelligence(IntelligenceBase):
    id: int
    timestamp: datetime
    status: str
    
    class Config:
        from_attributes = True

class CompetitorBase(BaseModel):
    domain: str
    company_name: str
    metadata: Optional[Dict[str, Any]] = {}

class CompetitorCreate(CompetitorBase):
    pass

class Competitor(CompetitorBase):
    id: int
    added_date: datetime
    active: bool
    
    class Config:
        from_attributes = True

class HeadStatus(BaseModel):
    head_name: str
    status: str
    last_run: Optional[datetime]
    next_run: Optional[datetime]
    discoveries_count: int
    error_count: int
    
    class Config:
        from_attributes = True

class DashboardStats(BaseModel):
    total_discoveries: int
    critical_threats: int
    high_threats: int
    active_competitors: int
    active_heads: int
    last_24h_discoveries: int
    top_threat_competitor: Optional[str]

class WebSocketMessage(BaseModel):
    type: str  # intelligence, status, alert
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HeadConfig(BaseModel):
    head_name: str
    enabled: bool
    check_interval: int  # seconds
    config: Dict[str, Any]

class AlertConfig(BaseModel):
    threat_level: ThreatLevelEnum
    channels: List[str]  # email, slack, webhook
    recipients: List[str]

class BulkIntelligenceQuery(BaseModel):
    competitors: Optional[List[str]] = None
    heads: Optional[List[str]] = None
    threat_levels: Optional[List[ThreatLevelEnum]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100
