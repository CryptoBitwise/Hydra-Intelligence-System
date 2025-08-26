# backend/heads/tech_radar.py
import asyncio
import httpx
from typing import List, Dict, Any
from datetime import datetime
import re
import json

class TechRadarHead:
    """
    Monitors competitor technology adoption.
    Detects: stack changes, infrastructure updates, API usage.
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.name = "TechRadar"
        self.monitoring = False
        self.tech_fingerprints = {}
        
        # Technology detection patterns
        self.tech_signals = {
            # Frontend
            'react': {'category': 'frontend', 'significance': 'medium'},
            'vue': {'category': 'frontend', 'significance': 'medium'},
            'angular': {'category': 'frontend', 'significance': 'medium'},
            'next.js': {'category': 'frontend', 'significance': 'high'},
            
            # Backend
            'graphql': {'category': 'api', 'significance': 'high'},
            'kubernetes': {'category': 'infrastructure', 'significance': 'critical'},
            'serverless': {'category': 'infrastructure', 'significance': 'high'},
            
            # AI/ML
            'tensorflow': {'category': 'ai', 'significance': 'critical'},
            'pytorch': {'category': 'ai', 'significance': 'critical'},
            'openai': {'category': 'ai', 'significance': 'critical'},
            
            # Analytics
            'segment': {'category': 'analytics', 'significance': 'medium'},
            'mixpanel': {'category': 'analytics', 'significance': 'medium'},
            'datadog': {'category': 'monitoring', 'significance': 'high'},
            
            # CDN/Performance
            'cloudflare': {'category': 'cdn', 'significance': 'medium'},
            'fastly': {'category': 'cdn', 'significance': 'high'},
            'vercel': {'category': 'hosting', 'significance': 'high'}
        }
    
    async def start_monitoring(self, competitors: List[str]):
        """Monitor competitor tech stacks"""
        self.monitoring = True
        
        while self.monitoring:
            for competitor in competitors:
                try:
                    # Multi-source tech detection
                    tech_stack = await self.detect_technologies(competitor)
                    
                    # Analyze changes
                    changes = self.analyze_tech_changes(competitor, tech_stack)
                    
                    if changes['significant_changes']:
                        intel = self.create_intelligence(competitor, changes)
                        await self.brain.process_intelligence(intel)
                    
                    # Update fingerprint
                    self.tech_fingerprints[competitor] = tech_stack
                    
                except Exception as e:
                    print(f"❌ TechRadar error for {competitor}: {e}")
                
                await asyncio.sleep(7200)  # Check every 2 hours
    
    async def detect_technologies(self, competitor: str) -> Dict:
        """Detect technologies across multiple sources"""
        tech_stack = {
            'frontend': [],
            'backend': [],
            'infrastructure': [],
            'analytics': [],
            'ai_ml': [],
            'apis': [],
            'security': [],
            'detected_at': datetime.now().isoformat()
        }
        
        # Method 1: Website analysis
        website_tech = await self.analyze_website(competitor)
        
        # Method 2: DNS & subdomain enumeration  
        dns_tech = await self.analyze_dns(competitor)
        
        # Method 3: GitHub repos (if public)
        github_tech = await self.analyze_github(competitor)
        
        # Method 4: Job postings tech requirements
        job_tech = await self.extract_tech_from_jobs(competitor)
        
        # Method 5: Public API analysis
        api_tech = await self.analyze_apis(competitor)
        
        # Merge all findings
        tech_stack = self.merge_tech_findings(
            website_tech, dns_tech, github_tech, job_tech, api_tech
        )
        
        return tech_stack
    
    async def analyze_website(self, competitor: str) -> Dict:
        """Analyze website for technology signals"""
        tech_found = {
            'frontend': [],
            'analytics': [],
            'cdn': [],
            'frameworks': []
        }
        
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(
                    f"https://{competitor}",
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                html = response.text
                headers = response.headers
                
                # Check response headers
                if 'x-powered-by' in headers:
                    tech_found['backend'].append(headers['x-powered-by'])
                
                if 'server' in headers:
                    server = headers['server'].lower()
                    if 'cloudflare' in server:
                        tech_found['cdn'].append('cloudflare')
                    elif 'amazon' in server:
                        tech_found['cdn'].append('aws')
                
                # Check HTML for frameworks
                if 'react' in html or '_react' in html:
                    tech_found['frontend'].append('react')
                
                if 'vue' in html or 'Vue.js' in html:
                    tech_found['frontend'].append('vue')
                
                if 'angular' in html:
                    tech_found['frontend'].append('angular')
                
                # Check for analytics
                if 'google-analytics' in html or 'gtag' in html:
                    tech_found['analytics'].append('google-analytics')
                
                if 'segment.com' in html:
                    tech_found['analytics'].append('segment')
                
                if 'mixpanel' in html:
                    tech_found['analytics'].append('mixpanel')
                
        except Exception as e:
            print(f"Website analysis error: {e}")
        
        return tech_found
    
    async def analyze_github(self, competitor: str) -> Dict:
        """Analyze public GitHub repos"""
        tech_found = {'languages': [], 'frameworks': [], 'dependencies': []}
        
        # Search for company GitHub
        # In production, use GitHub API
        try:
            # Check package.json, requirements.txt, go.mod, etc.
            pass
        except:
            pass
        
        return tech_found
    
    async def analyze_dns(self, competitor: str) -> Dict:
        """Analyze DNS records and subdomains"""
        findings = {'subdomains': [], 'services': []}
        
        # Check for common subdomains that reveal tech
        subdomains_to_check = [
            'api', 'app', 'admin', 'dashboard', 'staging',
            'dev', 'beta', 'mobile', 'graphql', 'ws', 'socket'
        ]
        
        # In production, use DNS enumeration tools
        # This reveals infrastructure choices
        
        return findings
    
    async def extract_tech_from_jobs(self, competitor: str) -> Dict:
        """Extract tech requirements from job postings"""
        # Reuse JobSpy data
        return {'required_skills': [], 'nice_to_have': []}
    
    async def analyze_apis(self, competitor: str) -> Dict:
        """Analyze public APIs if available"""
        api_info = {'endpoints': [], 'technologies': []}
        
        # Check for public API documentation
        # GraphQL introspection
        # REST API patterns
        
        return api_info
    
    def analyze_tech_changes(self, competitor: str, current_stack: Dict) -> Dict:
        """Detect significant technology changes"""
        changes = {
            'significant_changes': False,
            'new_technologies': [],
            'removed_technologies': [],
            'category_shifts': [],
            'risk_assessment': '',
            'opportunity_assessment': ''
        }
        
        if competitor not in self.tech_fingerprints:
            return changes
        
        old_stack = self.tech_fingerprints[competitor]
        
        # Find new technologies
        for category, techs in current_stack.items():
            if category == 'detected_at':
                continue
                
            old_techs = set(old_stack.get(category, []))
            new_techs = set(techs)
            
            added = new_techs - old_techs
            removed = old_techs - new_techs
            
            if added:
                for tech in added:
                    changes['new_technologies'].append({
                        'technology': tech,
                        'category': category,
                        'significance': self.assess_significance(tech)
                    })
                    changes['significant_changes'] = True
            
            if removed:
                for tech in removed:
                    changes['removed_technologies'].append({
                        'technology': tech,
                        'category': category
                    })
        
        # Assess strategic implications
        changes = self.assess_strategic_implications(changes)
        
        return changes
    
    def assess_significance(self, technology: str) -> str:
        """Assess the significance of a technology adoption"""
        tech_lower = technology.lower()
        
        for pattern, info in self.tech_signals.items():
            if pattern in tech_lower:
                return info['significance']
        
        return 'low'
    
    def assess_strategic_implications(self, changes: Dict) -> Dict:
        """Assess strategic implications of tech changes"""
        
        # Check for AI adoption
        ai_techs = [t for t in changes['new_technologies'] 
                   if 'ai' in t['category'] or 'tensorflow' in t['technology'].lower()]
        
        if ai_techs:
            changes['risk_assessment'] = 'HIGH: Competitor adopting AI technologies'
            changes['opportunity_assessment'] = 'Partner with AI vendors before competitor locks exclusivity'
        
        # Check for infrastructure scaling
        scale_techs = [t for t in changes['new_technologies']
                      if t['technology'].lower() in ['kubernetes', 'serverless', 'cdn']]
        
        if scale_techs:
            changes['risk_assessment'] = 'MEDIUM: Competitor preparing to scale'
            changes['opportunity_assessment'] = 'Focus on premium features while they handle scale issues'
        
        return changes
    
    def create_intelligence(self, competitor: str, changes: Dict):
        """Create intelligence report from tech changes"""
        from backend.core.brain import Intelligence, ThreatLevel
        
        # Determine threat level
        threat = ThreatLevel.LOW
        critical_techs = [t for t in changes['new_technologies'] 
                         if t['significance'] == 'critical']
        
        if critical_techs:
            threat = ThreatLevel.CRITICAL
        elif len(changes['new_technologies']) > 5:
            threat = ThreatLevel.HIGH
        elif changes['new_technologies']:
            threat = ThreatLevel.MEDIUM
        
        discovery = f"Tech stack changes: {len(changes['new_technologies'])} new, {len(changes['removed_technologies'])} removed"
        
        if critical_techs:
            discovery += f". Critical: {', '.join([t['technology'] for t in critical_techs[:3]])}"
        
        return Intelligence(
            head=self.name,
            competitor=competitor,
            discovery=discovery,
            threat_level=threat,
            confidence=0.9,
            timestamp=datetime.now(),
            data=changes,
            recommended_action=self.recommend_action(changes)
        )
    
    def recommend_action(self, changes: Dict) -> str:
        """Strategic recommendations based on tech changes"""
        
        if changes['risk_assessment'].startswith('HIGH'):
            return changes['opportunity_assessment']
        
        if any('kubernetes' in t['technology'].lower() for t in changes['new_technologies']):
            return "Competitor scaling infrastructure. Review your scaling strategy and consider microservices."
        
        if any('ai' in t['category'] for t in changes['new_technologies']):
            return "AI adoption detected. Evaluate AI integration opportunities or risk falling behind."
        
        return "Document technology changes and update competitive analysis."
    
    def merge_tech_findings(self, *sources) -> Dict:
        """Merge findings from multiple sources"""
        merged = {
            'frontend': [],
            'backend': [],
            'infrastructure': [],
            'analytics': [],
            'ai_ml': [],
            'apis': [],
            'security': [],
            'detected_at': datetime.now().isoformat()
        }
        
        for source in sources:
            for category, techs in source.items():
                if category in merged and isinstance(techs, list):
                    merged[category].extend(techs)
        
        # Deduplicate
        for category in merged:
            if isinstance(merged[category], list):
                merged[category] = list(set(merged[category]))
        
        return merged
    
    async def deep_investigate(self, competitor: str, trigger: str):
        """Deep investigation when triggered by another head"""
        print(f"📡 TechRadar: Deep scanning {competitor} infrastructure...")
        
        # Do thorough subdomain enumeration
        # Check for staging/development environments
        # Look for exposed APIs
        # Check cloud provider usage
        
        return {"competitor": competitor, "trigger": trigger, "tech_scan": "complete"}
