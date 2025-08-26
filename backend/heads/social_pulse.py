# backend/heads/social_pulse.py
import asyncio
import httpx
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
from textblob import TextBlob  # For sentiment analysis

class SocialPulseHead:
    """
    Monitors social media sentiment and brand perception.
    Tracks: customer complaints, viral issues, PR crises, positive momentum.
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.name = "SocialPulse"
        self.monitoring = False
        self.sentiment_history = {}
        self.platforms = ['twitter', 'reddit', 'hackernews', 'linkedin']
        
    async def start_monitoring(self, competitors: List[str]):
        """Monitor social sentiment"""
        self.monitoring = True
        
        while self.monitoring:
            for competitor in competitors:
                try:
                    # Gather social mentions
                    mentions = await self.gather_social_mentions(competitor)
                    
                    # Analyze sentiment
                    analysis = self.analyze_sentiment(competitor, mentions)
                    
                    if analysis['significant_change']:
                        intel = self.create_intelligence(competitor, analysis)
                        await self.brain.process_intelligence(intel)
                    
                    # Update history
                    self.sentiment_history[competitor] = analysis
                    
                except Exception as e:
                    print(f"❌ SocialPulse error for {competitor}: {e}")
                
                await asyncio.sleep(1800)  # Check every 30 minutes
    
    async def gather_social_mentions(self, competitor: str) -> List[Dict]:
        """Gather mentions across social platforms via Bright Data"""
        
        bright_data_config = {
            "collector": "social_mentions",
            "parameters": {
                "keywords": [competitor, f"@{competitor}", f"#{competitor}"],
                "platforms": self.platforms,
                "time_range": "24h",
                "fields": [
                    "text", "author", "timestamp", "likes", 
                    "shares", "comments", "url", "platform"
                ]
            }
        }
        
        mentions = []
        
        # Simulate social data collection
        # In production, this calls Bright Data API
        
        sample_mentions = [
            {
                'text': f"{competitor} just raised prices again. Switching to alternative.",
                'platform': 'twitter',
                'author': 'user123',
                'likes': 45,
                'timestamp': datetime.now().isoformat(),
                'sentiment': None  # Will be analyzed
            },
            {
                'text': f"Love the new feature from {competitor}! Game changer!",
                'platform': 'reddit',
                'author': 'user456',
                'likes': 120,
                'timestamp': datetime.now().isoformat(),
                'sentiment': None
            }
        ]
        
        return sample_mentions
    
    def analyze_sentiment(self, competitor: str, mentions: List[Dict]) -> Dict:
        """Analyze sentiment trends and detect issues"""
        
        analysis = {
            'total_mentions': len(mentions),
            'sentiment_score': 0,
            'sentiment_trend': 'neutral',
            'positive_mentions': 0,
            'negative_mentions': 0,
            'neutral_mentions': 0,
            'viral_posts': [],
            'issues_detected': [],
            'opportunities': [],
            'significant_change': False,
            'platform_breakdown': {}
        }
        
        if not mentions:
            return analysis
        
        sentiments = []
        
        for mention in mentions:
            # Analyze sentiment
            blob = TextBlob(mention['text'])
            sentiment = blob.sentiment.polarity  # -1 to 1
            mention['sentiment'] = sentiment
            sentiments.append(sentiment)
            
            # Categorize
            if sentiment > 0.1:
                analysis['positive_mentions'] += 1
            elif sentiment < -0.1:
                analysis['negative_mentions'] += 1
            else:
                analysis['neutral_mentions'] += 1
            
            # Check for viral posts (high engagement)
            engagement = mention.get('likes', 0) + mention.get('shares', 0) * 2
            if engagement > 100:
                analysis['viral_posts'].append({
                    'text': mention['text'][:200],
                    'engagement': engagement,
                    'sentiment': sentiment,
                    'platform': mention['platform']
                })
            
            # Detect specific issues
            text_lower = mention['text'].lower()
            if 'bug' in text_lower or 'broken' in text_lower:
                analysis['issues_detected'].append('Technical issues mentioned')
            if 'expensive' in text_lower or 'price' in text_lower:
                analysis['issues_detected'].append('Price complaints')
            if 'slow' in text_lower or 'down' in text_lower:
                analysis['issues_detected'].append('Performance issues')
            if 'support' in text_lower and sentiment < 0:
                analysis['issues_detected'].append('Support complaints')
        
        # Calculate average sentiment
        analysis['sentiment_score'] = sum(sentiments) / len(sentiments) if sentiments else 0
        
        # Determine trend
        if competitor in self.sentiment_history:
            old_score = self.sentiment_history[competitor].get('sentiment_score', 0)
            change = analysis['sentiment_score'] - old_score
            
            if abs(change) > 0.2:
                analysis['significant_change'] = True
                analysis['sentiment_trend'] = 'improving' if change > 0 else 'declining'
        
        # Platform breakdown
        for platform in self.platforms:
            platform_mentions = [m for m in mentions if m.get('platform') == platform]
            if platform_mentions:
                platform_sentiments = [m['sentiment'] for m in platform_mentions]
                analysis['platform_breakdown'][platform] = {
                    'count': len(platform_mentions),
                    'avg_sentiment': sum(platform_sentiments) / len(platform_sentiments)
                }
        
        # Identify opportunities
        if analysis['negative_mentions'] > analysis['positive_mentions'] * 2:
            analysis['opportunities'].append('Competitor facing backlash - opportunity to win customers')
        
        if any('switching' in m['text'].lower() for m in mentions):
            analysis['opportunities'].append('Customers actively looking for alternatives')
        
        return analysis
    
    def create_intelligence(self, competitor: str, analysis: Dict):
        """Create intelligence from sentiment analysis"""
        from backend.core.brain import Intelligence, ThreatLevel
        
        # Determine threat level
        threat = ThreatLevel.LOW
        
        if analysis['viral_posts'] and analysis['sentiment_score'] < -0.3:
            threat = ThreatLevel.CRITICAL  # PR crisis
        elif analysis['sentiment_trend'] == 'declining' and analysis['significant_change']:
            threat = ThreatLevel.HIGH
        elif analysis['opportunities']:
            threat = ThreatLevel.MEDIUM  # Opportunity to act
        
        discovery = f"Sentiment: {analysis['sentiment_score']:.2f} "
        discovery += f"({analysis['positive_mentions']}↑ {analysis['negative_mentions']}↓) "
        
        if analysis['viral_posts']:
            discovery += f"| {len(analysis['viral_posts'])} viral posts "
        
        if analysis['issues_detected']:
            discovery += f"| Issues: {', '.join(set(analysis['issues_detected'][:3]))}"
        
        return Intelligence(
            head=self.name,
            competitor=competitor,
            discovery=discovery,
            threat_level=threat,
            confidence=0.8,
            timestamp=datetime.now(),
            data=analysis,
            recommended_action=self.recommend_action(analysis)
        )
    
    def recommend_action(self, analysis: Dict) -> str:
        """Recommend actions based on sentiment"""
        
        if analysis['sentiment_score'] < -0.5 and analysis['viral_posts']:
            return "URGENT: Competitor in PR crisis. Launch 'switch to us' campaign immediately."
        
        if 'Technical issues mentioned' in analysis['issues_detected']:
            return "Competitor has reliability issues. Emphasize your uptime in marketing."
        
        if 'Price complaints' in analysis['issues_detected']:
            return "Price sensitivity detected. Consider targeted discount for switchers."
        
        if analysis['opportunities']:
            return f"Opportunity: {analysis['opportunities'][0]}"
        
        return "Monitor sentiment. Prepare response strategies."
    
    async def deep_investigate(self, competitor: str, trigger: str):
        """Deep investigation when triggered"""
        print(f"💭 SocialPulse: Deep sentiment scan on {competitor}...")
        
        # Expand search to more platforms
        # Check employee sentiment on Glassdoor
        # Check customer reviews
        # Check news sentiment
        
        return {"competitor": competitor, "expanded_sentiment": "complete"}
