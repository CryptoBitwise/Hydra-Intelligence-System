import asyncio
from typing import List, Dict, Any
from datetime import datetime

from typing import Dict, Any, List


class TechRadarHead:
    def __init__(self, brain=None):
        self.brain = brain
        self.name = "TechRadar"
        self.monitoring = False
        self.tech_fingerprints: Dict[str, Dict[str, Any]] = {}

    async def start_monitoring(self, competitors: List[str]):
        self.monitoring = True
        while self.monitoring:
            for competitor in competitors:
                try:
                    tech_stack = await self.detect_technologies(competitor)
                    changes = self.analyze_tech_changes(competitor, tech_stack)
                    if changes["significant_changes"]:
                        await self.brain.process_intelligence(self.create_intelligence(competitor, changes))
                    self.tech_fingerprints[competitor] = tech_stack
                except Exception:
                    pass
                await asyncio.sleep(7200)

    async def detect_technologies(self, competitor: str) -> Dict[str, Any]:
        return {
            "frontend": [],
            "backend": [],
            "infrastructure": [],
            "analytics": [],
            "ai_ml": [],
            "apis": [],
            "security": [],
            "detected_at": datetime.now().isoformat(),
        }

    def analyze_tech_changes(self, competitor: str, current_stack: Dict[str, Any]) -> Dict[str, Any]:
        changes: Dict[str, Any] = {
            "significant_changes": False,
            "new_technologies": [],
            "removed_technologies": [],
            "category_shifts": [],
            "risk_assessment": "",
            "opportunity_assessment": "",
        }
        if competitor not in self.tech_fingerprints:
            return changes
        old_stack = self.tech_fingerprints[competitor]
        for category, techs in current_stack.items():
            if category == "detected_at":
                continue
            old_techs = set(old_stack.get(category, []))
            new_techs = set(techs)
            added = new_techs - old_techs
            removed = old_techs - new_techs
            if added:
                for tech in added:
                    changes["new_technologies"].append({"technology": tech, "category": category, "significance": "low"})
                    changes["significant_changes"] = True
            if removed:
                for tech in removed:
                    changes["removed_technologies"].append({"technology": tech, "category": category})
        return changes

    def create_intelligence(self, competitor: str, changes: Dict[str, Any]):
        threat = "medium" if changes.get("new_technologies") else "low"
        discovery = f"Tech stack changes: {len(changes['new_technologies'])} new, {len(changes['removed_technologies'])} removed"
        return {
            "head": self.name,
            "competitor": competitor,
            "discovery": discovery,
            "threat_level": threat,
            "confidence": 0.9,
            "data": changes,
        }

    def recommend_action(self, changes: Dict[str, Any]) -> str:
        if changes.get("new_technologies"):
            return "Document technology changes and update competitive analysis."
        return "Monitor for technology updates."

    async def analyze(self, competitor: str) -> Dict[str, Any]:
        stack = await self.detect_technologies(competitor)
        changes = self.analyze_tech_changes(competitor, stack)
        self.tech_fingerprints[competitor] = stack
        return self.create_intelligence(competitor, changes)


