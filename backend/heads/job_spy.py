# backend/heads/job_spy.py
import asyncio
import httpx
from typing import List, Dict, Any
from datetime import datetime
import json
import re

class JobSpyHead:
    """
    Monitors competitor hiring patterns.
    Reveals: expansion plans, tech stack changes, strategic pivots.
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.name = "JobSpy"
        self.monitoring = False
        self.job_history = {}
        self.tech_patterns = {
            'react': 'Frontend modernization',
            'kubernetes': 'Scaling infrastructure',
            'rust': 'Performance optimization',
            'flutter': 'Mobile expansion',
            'ai|machine learning|ml': 'AI investment',
            'blockchain|web3|crypto': 'Web3 pivot',
            'salesforce': 'Enterprise focus',
            'aws|azure|gcp': 'Cloud migration'
        }
        
    async def start_monitoring(self, competitors: List[str]):
        """Monitor competitor job postings"""
        self.monitoring = True
        
        while self.monitoring:
            for competitor in competitors:
                try:
                    # Scrape job postings
                    jobs = await self.scrape_jobs(competitor)
                    
                    # Analyze patterns
                    analysis = self.analyze_hiring_patterns(competitor, jobs)
                    
                    if analysis['significant_changes']:
                        intel = self.create_intelligence(competitor, analysis)
                        await self.brain.process_intelligence(intel)
                    
                    # Update history
                    self.job_history[competitor] = jobs
                    
                except Exception as e:
                    print(f"❌ JobSpy error for {competitor}: {e}")
                
                await asyncio.sleep(3600)  # Check hourly
    
    async def scrape_jobs(self, competitor: str) -> List[Dict]:
        """Scrape job postings via Bright Data"""
        # Bright Data configuration for job boards
        bright_data_params = {
            "collector": "job_boards",
            "parameters": {
                "company_names": [competitor],
                "sites": ["linkedin", "indeed", "glassdoor", "angellist"],
                "fields": [
                    "title", "department", "location", 
                    "requirements", "salary_range", "posted_date",
                    "job_description", "skills", "experience_level"
                ]
            }
        }
        
        # For demo: simulate with real structure
        jobs = []
        
        # LinkedIn scraping simulation
        async with httpx.AsyncClient() as client:
            # In production, this goes through Bright Data
            response = await client.post(
                "http://localhost:11434/api/generate",  # Using Ollama to simulate
                json={
                    "model": "llama3.1:8b",
                    "prompt": f"Generate 3 realistic job postings for {competitor} that reveal strategic direction. Format as JSON.",
                    "stream": False
                }
            )
            
            # Parse and structure jobs
            jobs = self.parse_job_listings(response.json())
            
        return jobs
    
    def analyze_hiring_patterns(self, competitor: str, current_jobs: List[Dict]) -> Dict:
        """Detect strategic shifts from hiring patterns"""
        analysis = {
            'significant_changes': False,
            'new_departments': [],
            'tech_stack_changes': [],
            'expansion_locations': [],
            'hiring_velocity': 0,
            'strategic_indicators': [],
            'estimated_burn_rate': 0
        }
        
        if competitor not in self.job_history:
            # First scan
            self.job_history[competitor] = current_jobs
            return analysis
        
        old_jobs = self.job_history[competitor]
        
        # Detect department expansion
        current_depts = {job.get('department') for job in current_jobs}
        old_depts = {job.get('department') for job in old_jobs}
        new_depts = current_depts - old_depts
        
        if new_depts:
            analysis['new_departments'] = list(new_depts)
            analysis['significant_changes'] = True
        
        # Detect tech stack changes
        all_requirements = ' '.join([job.get('requirements', '') for job in current_jobs]).lower()
        
        for pattern, indicator in self.tech_patterns.items():
            if re.search(pattern, all_requirements):
                if indicator not in analysis['tech_stack_changes']:
                    analysis['tech_stack_changes'].append(indicator)
                    analysis['significant_changes'] = True
        
        # Calculate hiring velocity
        analysis['hiring_velocity'] = len(current_jobs) - len(old_jobs)
        
        # Estimate burn rate from hiring
        senior_roles = sum(1 for job in current_jobs if 'senior' in job.get('title', '').lower())
        analysis['estimated_burn_rate'] = (len(current_jobs) * 120000 + senior_roles * 50000) / 12
        
        # Strategic indicators
        if analysis['hiring_velocity'] > 10:
            analysis['strategic_indicators'].append('Rapid expansion phase')
        
        if 'AI' in analysis['tech_stack_changes']:
            analysis['strategic_indicators'].append('Building AI capabilities')
            
        if any('sales' in dept.lower() for dept in analysis['new_departments']):
            analysis['strategic_indicators'].append('Sales push incoming')
        
        return analysis
    
    def create_intelligence(self, competitor: str, analysis: Dict):
        """Create intelligence report from job analysis"""
        from backend.core.brain import Intelligence, ThreatLevel
        
        # Assess threat level based on findings
        threat = ThreatLevel.LOW
        
        if analysis['hiring_velocity'] > 20:
            threat = ThreatLevel.CRITICAL
        elif analysis['hiring_velocity'] > 10:
            threat = ThreatLevel.HIGH
        elif analysis['tech_stack_changes']:
            threat = ThreatLevel.MEDIUM
        
        discovery = f"Hiring pattern change detected: "
        discoveries = []
        
        if analysis['new_departments']:
            discoveries.append(f"New departments: {', '.join(analysis['new_departments'])}")
        
        if analysis['tech_stack_changes']:
            discoveries.append(f"Tech focus: {', '.join(analysis['tech_stack_changes'][:3])}")
        
        if analysis['hiring_velocity'] > 0:
            discoveries.append(f"{analysis['hiring_velocity']} new positions")
        
        discovery += '; '.join(discoveries)
        
        action = self.recommend_action(analysis)
        
        return Intelligence(
            head=self.name,
            competitor=competitor,
            discovery=discovery,
            threat_level=threat,
            confidence=0.85,
            timestamp=datetime.now(),
            data=analysis,
            recommended_action=action
        )
    
    def recommend_action(self, analysis: Dict) -> str:
        """AI-powered strategic recommendations"""
        if 'AI investment' in analysis['tech_stack_changes']:
            return "URGENT: Competitor building AI team. Accelerate your AI roadmap or acquire AI startup."
        
        if analysis['hiring_velocity'] > 15:
            return "Competitor in hypergrowth. Consider: 1) Poach their talent 2) Prepare for aggressive competition"
        
        if 'Sales push incoming' in analysis['strategic_indicators']:
            return "Competitor scaling sales. Strengthen customer relationships and lock in contracts."
        
        return "Monitor situation. Update competitive battle cards."
    
    def parse_job_listings(self, raw_data: Dict) -> List[Dict]:
        """Parse job listings from various sources"""
        # Implementation depends on source
        # This is a simplified version
        jobs = []
        
        # Parse the response and extract jobs
        # In production, this would parse real job board data
        
        return jobs

    async def deep_investigate(self, competitor: str, trigger: str):
        """When another head triggers investigation"""
        # Do focused job analysis
        print(f"🎯 JobSpy: Deep scanning {competitor} hiring...")
        
        # Look for specific roles related to trigger
        if 'price' in trigger.lower():
            # Check for pricing analysts, revenue ops
            roles_to_check = ['pricing', 'revenue', 'analytics']
        elif 'tech' in trigger.lower():
            # Check for engineers
            roles_to_check = ['engineer', 'developer', 'architect']
        else:
            roles_to_check = []
        
        # Return focused analysis
        return {"focus_area": roles_to_check, "competitor": competitor}
