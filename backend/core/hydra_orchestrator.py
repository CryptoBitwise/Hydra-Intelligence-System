# backend/core/hydra_orchestrator.py
import asyncio
from typing import List
from backend.core.brain import HydraBrain
from backend.heads.price_watch import PriceWatchHead
from backend.heads.job_spy import JobSpyHead
from backend.heads.tech_radar import TechRadarHead
from backend.heads.social_pulse import SocialPulseHead
from backend.heads.patent_hawk import PatentHawkHead
from backend.heads.ad_tracker import AdTrackerHead

async def initialize_hydra(competitors: List[str]):
    """Initialize HYDRA with all 6 heads"""
    
    # Create the brain
    brain = HydraBrain()
    brain.set_competitors(competitors)
    
    # Create and attach all heads
    heads = {
        'PriceWatch': PriceWatchHead(brain),
        'JobSpy': JobSpyHead(brain),
        'TechRadar': TechRadarHead(brain),
        'SocialPulse': SocialPulseHead(brain),
        'PatentHawk': PatentHawkHead(brain),
        'AdTracker': AdTrackerHead(brain)
    }
    
    for name, head in heads.items():
        await brain.attach_head(name, head)
    
    print(f"""
    ╔════════════════════════════════════════════════╗
    ║              🐉 HYDRA INITIALIZED 🐉              ║
    ║                                                  ║
    ║  6 HEADS ACTIVE:                                ║
    ║  👁️  PriceWatch  - Monitoring prices            ║
    ║  🎯 JobSpy      - Tracking talent               ║
    ║  📡 TechRadar   - Detecting tech                ║
    ║  💭 SocialPulse - Analyzing sentiment           ║
    ║  📋 PatentHawk  - Watching innovation           ║
    ║  📊 AdTracker   - Following campaigns           ║
    ║                                                  ║
    ║  TARGETS LOCKED: {', '.join(competitors)}       ║
    ║                                                  ║
    ║         TOTAL MARKET DOMINANCE INCOMING         ║
    ╚════════════════════════════════════════════════╝
    """)
    
    # Start the brain
    await brain.start()

if __name__ == "__main__":
    # Define your competitors
    COMPETITORS = [
        "competitor1.com",
        "competitor2.com",
        "competitor3.com"
    ]
    
    # Run HYDRA
    asyncio.run(initialize_hydra(COMPETITORS))
