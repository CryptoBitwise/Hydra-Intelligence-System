"""
HYDRA Brain Controller
Central nervous system that coordinates all heads and manages data flow
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json

from .config import config
from .database import get_db, Alert, SystemHealth, AnalysisResult
from ..ml.analyzer import HydraAnalyzer
from ..ml.patterns import PatternRecognizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HeadStatus(Enum):
    """Status of HYDRA heads"""
    IDLE = "idle"
    SCANNING = "scanning"
    PROCESSING = "processing"
    ERROR = "error"
    DISABLED = "disabled"

@dataclass
class HeadState:
    """State information for each head"""
    name: str
    status: HeadStatus
    last_scan: Optional[datetime]
    next_scan: Optional[datetime]
    data_count: int
    error_count: int
    performance_score: float

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Intelligence:
    """Single piece of competitive intelligence"""
    head: str  # Which head discovered this
    competitor: str
    discovery: str
    threat_level: ThreatLevel
    confidence: float
    timestamp: datetime
    data: Dict[str, Any]
    recommended_action: str

class HydraBrain:
    """
    The central brain that coordinates all 6 heads.
    This is where the magic happens.
    """
    
    def __init__(self):
        self.heads = {}
        self.intelligence_queue = asyncio.Queue()
        self.alert_thresholds = {
            ThreatLevel.CRITICAL: 0.9,
            ThreatLevel.HIGH: 0.7,
            ThreatLevel.MEDIUM: 0.5,
            ThreatLevel.LOW: 0.3
        }
        self.competitors = []
        self.running = False
        logger.info("🧠 HydraBrain initialized")

    async def attach_head(self, name: str, head_instance):
        """Attach a new head to Hydra"""
        self.heads[name] = head_instance
        logger.info(f"🐉 HYDRA: {name} head attached")

    def set_competitors(self, competitors: List[str]):
        """Define which competitors to monitor"""
        self.competitors = competitors
        logger.info(f"🎯 HYDRA targeting: {', '.join(competitors)}")

    async def process_intelligence(self, intel: Intelligence):
        """Process incoming intelligence from any head"""
        logger.info(f"🧠 Processing intelligence from {intel.head}: {intel.discovery}")
        
        # Analyze with local LLM
        analysis = await self.analyze_with_ollama(intel)
        
        # Determine if other heads should investigate
        if intel.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            await self.coordinate_heads(intel)
        
        # Store in database
        await self.store_intelligence(intel)
        
        # Send alerts if needed
        if intel.confidence >= self.alert_thresholds[intel.threat_level]:
            await self.send_alert(intel)
        
        return analysis

    async def analyze_with_ollama(self, intel: Intelligence):
        """Use local LLM for deep analysis"""
        prompt = f"""
        Analyze this competitive intelligence:
        
        Competitor: {intel.competitor}
        Discovery: {intel.discovery}
        Source: {intel.head}
        Data: {json.dumps(intel.data, indent=2)}
        
        Provide:
        1. Business impact assessment
        2. Recommended response strategy
        3. Urgency level (1-10)
        4. Additional data needed
        
        Be specific and actionable.
        """
        
        try:
            # This will run on your 4090 via Ollama
            import ollama
            response = ollama.generate(
                model='llama3.1:8b',
                prompt=prompt
            )
            logger.info("🤖 Ollama analysis completed")
            return response['response']
        except Exception as e:
            logger.error(f"🤖 Ollama analysis failed: {e}")
            return "Analysis failed - using fallback logic"

    async def coordinate_heads(self, trigger_intel: Intelligence):
        """When one head finds something big, others investigate"""
        logger.info(f"🚨 HYDRA: All heads focusing on {trigger_intel.competitor}")
        
        tasks = []
        for head_name, head in self.heads.items():
            if head_name != trigger_intel.head:
                # Tell other heads to investigate
                task = head.deep_investigate(
                    trigger_intel.competitor,
                    trigger_intel.discovery
                )
                tasks.append(task)
        
        # All heads attack simultaneously
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def store_intelligence(self, intel: Intelligence):
        """Store intelligence in database"""
        logger.info(f"💾 Storing intelligence from {intel.head}")
        # TODO: Implement database storage
        pass

    async def send_alert(self, intel: Intelligence):
        """Send alert based on intelligence"""
        logger.info(f"🚨 Sending alert for {intel.threat_level.value} threat from {intel.head}")
        # TODO: Implement alert system
        pass

    async def start(self):
        """Start the Hydra brain"""
        self.running = True
        logger.info("""
        ╔════════════════════════════════════════╗
        ║ HYDRA ACTIVATED                        ║
        ║ 6 HEADS, 1 PURPOSE:                    ║
        ║ TOTAL MARKET DOMINANCE                ║
        ╚════════════════════════════════════════╝
        """)
        
        # Start all heads
        tasks = []
        for name, head in self.heads.items():
            tasks.append(head.start_monitoring(self.competitors))
        
        await asyncio.gather(*tasks, return_exceptions=True)

    async def stop(self):
        """Stop the Hydra brain"""
        self.running = False
        logger.info("🛑 HYDRA brain stopped")

    def get_status(self) -> Dict[str, Any]:
        """Get current brain status"""
        return {
            "running": self.running,
            "heads_count": len(self.heads),
            "competitors": self.competitors,
            "queue_size": self.intelligence_queue.qsize(),
            "alert_thresholds": {k.value: v for k, v in self.alert_thresholds.items()}
        }

# Global brain instance
brain = HydraBrain()
