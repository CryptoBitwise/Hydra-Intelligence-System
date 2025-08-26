"""
HYDRA Configuration
Central configuration for all HYDRA heads and services
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HydraConfig:
    """Central configuration for HYDRA system"""
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hydra:hydra@localhost:5432/hydra_db")
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_DEBUG = os.getenv("API_DEBUG", "False").lower() == "true"
    
    # WebSocket Configuration
    WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
    WS_PORT = int(os.getenv("WS_PORT", "8001"))
    
    # Bright Data Configuration
    BRIGHT_DATA_USERNAME = os.getenv("BRIGHT_DATA_USERNAME", "")
    BRIGHT_DATA_PASSWORD = os.getenv("BRIGHT_DATA_PASSWORD", "")
    BRIGHT_DATA_HOST = os.getenv("BRIGHT_DATA_HOST", "brd.superproxy.io")
    BRIGHT_DATA_PORT = int(os.getenv("BRIGHT_DATA_PORT", "22225"))
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    
    # ChromaDB Configuration
    CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
    CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
    
    # Head-specific configurations
    HEADS_CONFIG = {
        "price_watch": {
            "enabled": os.getenv("PRICE_WATCH_ENABLED", "True").lower() == "true",
            "scan_interval": int(os.getenv("PRICE_WATCH_INTERVAL", "300")),  # 5 minutes
            "targets": os.getenv("PRICE_WATCH_TARGETS", "").split(",") if os.getenv("PRICE_WATCH_TARGETS") else []
        },
        "job_spy": {
            "enabled": os.getenv("JOB_SPY_ENABLED", "True").lower() == "true",
            "scan_interval": int(os.getenv("JOB_SPY_INTERVAL", "600")),  # 10 minutes
            "companies": os.getenv("JOB_SPY_COMPANIES", "").split(",") if os.getenv("JOB_SPY_COMPANIES") else []
        },
        "tech_radar": {
            "enabled": os.getenv("TECH_RADAR_ENABLED", "True").lower() == "true",
            "scan_interval": int(os.getenv("TECH_RADAR_INTERVAL", "1800")),  # 30 minutes
            "tech_keywords": os.getenv("TECH_RADAR_KEYWORDS", "").split(",") if os.getenv("TECH_RADAR_KEYWORDS") else []
        },
        "social_pulse": {
            "enabled": os.getenv("SOCIAL_PULSE_ENABLED", "True").lower() == "true",
            "scan_interval": int(os.getenv("SOCIAL_PULSE_INTERVAL", "900")),  # 15 minutes
            "platforms": os.getenv("SOCIAL_PULSE_PLATFORMS", "twitter,linkedin,reddit").split(",")
        },
        "patent_hawk": {
            "enabled": os.getenv("PATENT_HAWK_ENABLED", "True").lower() == "true",
            "scan_interval": int(os.getenv("PATENT_HAWK_INTERVAL", "3600")),  # 1 hour
            "patent_offices": os.getenv("PATENT_HAWK_OFFICES", "uspto,epo,jpo").split(",")
        },
        "ad_tracker": {
            "enabled": os.getenv("AD_TRACKER_ENABLED", "True").lower() == "true",
            "scan_interval": int(os.getenv("AD_TRACKER_INTERVAL", "1200")),  # 20 minutes
            "ad_networks": os.getenv("AD_TRACKER_NETWORKS", "google,facebook,amazon").split(",")
        }
    }
    
    # Alert Configuration
    ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL", "")
    ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")
    
    # GPU Configuration (for 4090 analysis)
    GPU_ENABLED = os.getenv("GPU_ENABLED", "False").lower() == "true"
    GPU_DEVICE = os.getenv("GPU_DEVICE", "cuda:0")
    
    @classmethod
    def get_head_config(cls, head_name: str) -> Dict[str, Any]:
        """Get configuration for a specific head"""
        return cls.HEADS_CONFIG.get(head_name, {})
    
    @classmethod
    def is_head_enabled(cls, head_name: str) -> bool:
        """Check if a specific head is enabled"""
        config = cls.get_head_config(head_name)
        return config.get("enabled", False)

# Global config instance
config = HydraConfig()
