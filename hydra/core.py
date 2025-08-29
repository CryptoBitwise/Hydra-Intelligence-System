import sqlite3
import json
import asyncio
from datetime import datetime
from pathlib import Path
import yaml
from typing import List, Dict, Any


class HydraFree:
    """HYDRA - Actually FREE Competitive Intelligence"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self.load_config(config_path)
        self.db = self.init_database()
        
    def load_config(self, path: str) -> Dict:
        if Path(path).exists():
            with open(path, encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {
            "competitors": ["example.com"],
            "heads": ["PriceWatch", "JobSpy", "TechRadar"],
            "use_bright_data": False
        }
    
    def init_database(self) -> sqlite3.Connection:
        conn = sqlite3.connect("hydra.db")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                head TEXT,
                competitor TEXT,
                discovery TEXT,
                threat_level TEXT,
                confidence REAL,
                data TEXT,
                status TEXT DEFAULT 'new'
            )
        ''')
        conn.commit()
        return conn
    
    def save_intelligence(self, intel: Dict):
        self.db.execute('''
            INSERT INTO intelligence 
            (timestamp, head, competitor, discovery, threat_level, confidence, data)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            intel['head'],
            intel['competitor'],
            intel['discovery'],
            intel['threat_level'],
            intel['confidence'],
            json.dumps(intel.get('data', {}))
        ))
        self.db.commit()
    
    def get_recent_intelligence(self, hours: int = 24) -> List[Dict]:
        cursor = self.db.execute(f'''
            SELECT * FROM intelligence 
            WHERE datetime(timestamp) > datetime('now', '-{hours} hours')
            ORDER BY timestamp DESC
        ''')
        columns = [c[0] for c in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    async def collect_intelligence(self, competitors: List[str] = None):
        """Collect real intelligence using all heads"""
        from hydra.scrapers import scrape_intelligently
        
        competitors = competitors or self.config['competitors']
        saved = 0
        
        for competitor in competitors:
            print(f"\n🎯 Analyzing {competitor}...")
            
            # Run each head
            for head_name in self.config.get('heads', []):
                try:
                    # Import and run the head
                    if head_name == "PriceWatch":
                        from hydra.heads.price_watch import PriceWatchHead
                        head = PriceWatchHead(self)
                    elif head_name == "JobSpy":
                        from hydra.heads.job_spy import JobSpyHead
                        head = JobSpyHead(self)
                    elif head_name == "TechRadar":
                        from hydra.heads.tech_radar import TechRadarHead
                        head = TechRadarHead(self)
                    else:
                        continue
                    
                    # Analyze with the head
                    result = await head.analyze(competitor)
                    
                    if result:
                        self.save_intelligence(result)
                        saved += 1
                        
                        # Print summary
                        icon = "🔴" if result['threat_level'] == 'critical' else "🟡"
                        print(f"  {icon} {head_name}: {result['discovery'][:60]}...")
                        
                except Exception as e:
                    print(f"  ❌ {head_name} failed: {e}")
        
        return saved
    
    def export_dashboard(self, output_path: str = "dashboard/data.json"):
        Path("dashboard").mkdir(exist_ok=True)
        recent = self.get_recent_intelligence(24)
        
        stats = {
            "total_discoveries": len(recent),
            "critical_threats": sum(1 for i in recent if i.get('threat_level') == 'critical'),
            "high_threats": sum(1 for i in recent if i.get('threat_level') == 'high'),
            "competitors": list(set(i['competitor'] for i in recent)),
            "last_updated": datetime.now().isoformat()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"stats": stats, "intelligence": recent}, f, indent=2)
        
        return stats


