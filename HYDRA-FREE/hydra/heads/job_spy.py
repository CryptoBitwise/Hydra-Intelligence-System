import asyncio
from typing import List, Dict, Any
from datetime import datetime
import re

from typing import Optional


class JobSpyHead:
    def __init__(self, brain=None):
        self.brain = brain
        self.name = "JobSpy"
        self.monitoring = False
        self.job_history: Dict[str, List[Dict[str, Any]]] = {}
        self.tech_patterns = {
            "react": "Frontend modernization",
            "kubernetes": "Scaling infrastructure",
            "rust": "Performance optimization",
            "flutter": "Mobile expansion",
            "ai|machine learning|ml": "AI investment",
            "blockchain|web3|crypto": "Web3 pivot",
            "salesforce": "Enterprise focus",
            "aws|azure|gcp": "Cloud migration",
        }

    async def start_monitoring(self, competitors: List[str]):
        self.monitoring = True
        while self.monitoring:
            for competitor in competitors:
                try:
                    jobs = await self.scrape_jobs(competitor)
                    analysis = self.analyze_hiring_patterns(competitor, jobs)
                    if analysis["significant_changes"]:
                        await self.brain.process_intelligence(self.create_intelligence(competitor, analysis))
                    self.job_history[competitor] = jobs
                except Exception:
                    pass
                await asyncio.sleep(3600)

    async def scrape_jobs(self, competitor: str) -> List[Dict[str, Any]]:
        # Placeholder: implement free sources later
        return []

    def analyze_hiring_patterns(self, competitor: str, current_jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        analysis: Dict[str, Any] = {
            "significant_changes": False,
            "new_departments": [],
            "tech_stack_changes": [],
            "expansion_locations": [],
            "hiring_velocity": 0,
            "strategic_indicators": [],
            "estimated_burn_rate": 0,
        }
        if competitor not in self.job_history:
            self.job_history[competitor] = current_jobs
            return analysis
        old_jobs = self.job_history[competitor]
        current_depts = {job.get("department") for job in current_jobs}
        old_depts = {job.get("department") for job in old_jobs}
        new_depts = current_depts - old_depts
        if new_depts:
            analysis["new_departments"] = list(new_depts)
            analysis["significant_changes"] = True
        all_requirements = " ".join([job.get("requirements", "") for job in current_jobs]).lower()
        for pattern, indicator in self.tech_patterns.items():
            if re.search(pattern, all_requirements):
                if indicator not in analysis["tech_stack_changes"]:
                    analysis["tech_stack_changes"].append(indicator)
                    analysis["significant_changes"] = True
        analysis["hiring_velocity"] = len(current_jobs) - len(old_jobs)
        senior_roles = sum(1 for job in current_jobs if "senior" in job.get("title", "").lower())
        analysis["estimated_burn_rate"] = (len(current_jobs) * 120000 + senior_roles * 50000) / 12
        if analysis["hiring_velocity"] > 10:
            analysis["strategic_indicators"].append("Rapid expansion phase")
        if "AI" in analysis["tech_stack_changes"]:
            analysis["strategic_indicators"].append("Building AI capabilities")
        if any("sales" in (dept or "").lower() for dept in analysis["new_departments"]):
            analysis["strategic_indicators"].append("Sales push incoming")
        return analysis

    def create_intelligence(self, competitor: str, analysis: Dict[str, Any]):
        threat = "low"
        if analysis["hiring_velocity"] > 20:
            threat = "critical"
        elif analysis["hiring_velocity"] > 10:
            threat = "high"
        elif analysis["tech_stack_changes"]:
            threat = "medium"
        discoveries: List[str] = []
        if analysis["new_departments"]:
            discoveries.append(f"New departments: {', '.join(analysis['new_departments'])}")
        if analysis["tech_stack_changes"]:
            discoveries.append(f"Tech focus: {', '.join(analysis['tech_stack_changes'][:3])}")
        if analysis["hiring_velocity"] > 0:
            discoveries.append(f"{analysis['hiring_velocity']} new positions")
        discovery = "Hiring pattern change detected: " + "; ".join(discoveries)
        return {
            "head": self.name,
            "competitor": competitor,
            "discovery": discovery,
            "threat_level": threat,
            "confidence": 0.85,
            "data": analysis,
        }

    def recommend_action(self, analysis: Dict[str, Any]) -> str:
        if "AI investment" in analysis.get("tech_stack_changes", []):
            return "URGENT: Competitor building AI team. Accelerate your AI roadmap or acquire AI startup."
        if analysis.get("hiring_velocity", 0) > 15:
            return "Competitor in hypergrowth. Consider: 1) Poach talent 2) Prepare for aggressive competition"
        if "Sales push incoming" in analysis.get("strategic_indicators", []):
            return "Competitor scaling sales. Strengthen customer relationships and lock contracts."
        return "Monitor situation. Update competitive battle cards."

    async def analyze(self, competitor: str) -> Dict[str, Any]:
        jobs: List[Dict[str, Any]] = await self.scrape_jobs(competitor)
        analysis = self.analyze_hiring_patterns(competitor, jobs)
        self.job_history[competitor] = jobs
        return self.create_intelligence(competitor, analysis)


