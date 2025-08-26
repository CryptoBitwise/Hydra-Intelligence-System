"""
HYDRA Database Models
SQLAlchemy models for all HYDRA data
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Text, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import enum
import os
from typing import Optional

# Database URL - using PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:hydra123@localhost/hydra")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ThreatLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IntelligenceModel(Base):
    """Store all intelligence gathered by HYDRA"""
    __tablename__ = "intelligence"
    
    id = Column(Integer, primary_key=True, index=True)
    head = Column(String, index=True)  # Which head discovered this
    competitor = Column(String, index=True)
    discovery = Column(Text)
    threat_level = Column(SQLEnum(ThreatLevel))
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    data = Column(JSON)  # Store detailed data as JSON
    recommended_action = Column(Text)
    status = Column(String, default="new")  # new, acknowledged, acted_upon
    
class CompetitorModel(Base):
    """Track competitors being monitored"""
    __tablename__ = "competitors"
    
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    company_name = Column(String)
    added_date = Column(DateTime, default=datetime.utcnow)
    active = Column(Integer, default=1)  # Boolean as integer
    metadata = Column(JSON)  # Store additional info
    
class HeadStatusModel(Base):
    """Track status of each HYDRA head"""
    __tablename__ = "head_status"
    
    id = Column(Integer, primary_key=True, index=True)
    head_name = Column(String, unique=True, index=True)
    status = Column(String, default="inactive")  # active, inactive, error
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    discoveries_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    config = Column(JSON)

class AlertModel(Base):
    """Track alerts sent"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    intelligence_id = Column(Integer, index=True)
    alert_type = Column(String)  # email, slack, webhook
    sent_to = Column(String)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # sent, failed, pending
    response = Column(JSON)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
