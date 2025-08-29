import asyncio
from typing import List, Dict, Any
from datetime import datetime
from textblob import TextBlob


class SocialPulseHead:
    def __init__(self, brain=None):
        self.brain = brain
        self.name = "SocialPulse"
        self.monitoring = False
        self.sentiment_history: Dict[str, Dict[str, Any]] = {}
        self.platforms = ["twitter", "reddit", "hackernews", "linkedin"]

    async def start_monitoring(self, competitors: List[str]):
        self.monitoring = True
        while self.monitoring:
            for competitor in competitors:
                try:
                    mentions = await self.gather_social_mentions(competitor)
                    analysis = self.analyze_sentiment(competitor, mentions)
                    if analysis["significant_change"]:
                        await self.brain.process_intelligence(self.create_intelligence(competitor, analysis))
                    self.sentiment_history[competitor] = analysis
                except Exception:
                    pass
                await asyncio.sleep(1800)

    async def gather_social_mentions(self, competitor: str) -> List[Dict[str, Any]]:
        # Placeholder for free sources later
        return [
            {
                "text": f"{competitor} just raised prices again. Switching to alternative.",
                "platform": "twitter",
                "author": "user123",
                "likes": 45,
                "timestamp": datetime.now().isoformat(),
                "sentiment": None,
            },
            {
                "text": f"Love the new feature from {competitor}! Game changer!",
                "platform": "reddit",
                "author": "user456",
                "likes": 120,
                "timestamp": datetime.now().isoformat(),
                "sentiment": None,
            },
        ]

    def analyze_sentiment(self, competitor: str, mentions: List[Dict[str, Any]]) -> Dict[str, Any]:
        analysis: Dict[str, Any] = {
            "total_mentions": len(mentions),
            "sentiment_score": 0,
            "sentiment_trend": "neutral",
            "positive_mentions": 0,
            "negative_mentions": 0,
            "neutral_mentions": 0,
            "viral_posts": [],
            "issues_detected": [],
            "opportunities": [],
            "significant_change": False,
            "platform_breakdown": {},
        }
        if not mentions:
            return analysis
        sentiments: List[float] = []
        for mention in mentions:
            blob = TextBlob(mention["text"])  # -1..1
            sentiment = blob.sentiment.polarity
            mention["sentiment"] = sentiment
            sentiments.append(sentiment)
            if sentiment > 0.1:
                analysis["positive_mentions"] += 1
            elif sentiment < -0.1:
                analysis["negative_mentions"] += 1
            else:
                analysis["neutral_mentions"] += 1
            engagement = mention.get("likes", 0) + mention.get("shares", 0) * 2
            if engagement > 100:
                analysis["viral_posts"].append(
                    {
                        "text": mention["text"][:200],
                        "engagement": engagement,
                        "sentiment": sentiment,
                        "platform": mention["platform"],
                    }
                )
            text_lower = mention["text"].lower()
            if "bug" in text_lower or "broken" in text_lower:
                analysis["issues_detected"].append("Technical issues mentioned")
            if "expensive" in text_lower or "price" in text_lower:
                analysis["issues_detected"].append("Price complaints")
            if "slow" in text_lower or "down" in text_lower:
                analysis["issues_detected"].append("Performance issues")
            if "support" in text_lower and sentiment < 0:
                analysis["issues_detected"].append("Support complaints")
        analysis["sentiment_score"] = sum(sentiments) / len(sentiments) if sentiments else 0
        if competitor in self.sentiment_history:
            old_score = self.sentiment_history[competitor].get("sentiment_score", 0)
            change = analysis["sentiment_score"] - old_score
            if abs(change) > 0.2:
                analysis["significant_change"] = True
                analysis["sentiment_trend"] = "improving" if change > 0 else "declining"
        return analysis

    def create_intelligence(self, competitor: str, analysis: Dict[str, Any]):
        threat = "low"
        if analysis["viral_posts"] and analysis["sentiment_score"] < -0.3:
            threat = "critical"
        elif analysis["sentiment_trend"] == "declining" and analysis["significant_change"]:
            threat = "high"
        elif analysis["opportunities"]:
            threat = "medium"
        discovery = f"Sentiment: {analysis['sentiment_score']:.2f} ({analysis['positive_mentions']}↑ {analysis['negative_mentions']}↓)"
        if analysis["viral_posts"]:
            discovery += f" | {len(analysis['viral_posts'])} viral posts"
        if analysis["issues_detected"]:
            discovery += f" | Issues: {', '.join(set(analysis['issues_detected'][:3]))}"
        return {
            "head": self.name,
            "competitor": competitor,
            "discovery": discovery,
            "threat_level": threat,
            "confidence": 0.8,
            "data": analysis,
        }

    def recommend_action(self, analysis: Dict[str, Any]) -> str:
        if analysis["sentiment_score"] < -0.5 and analysis["viral_posts"]:
            return "URGENT: Competitor in PR crisis. Launch 'switch to us' campaign."
        if "Technical issues mentioned" in analysis["issues_detected"]:
            return "Competitor has reliability issues. Emphasize your uptime in marketing."
        if "Price complaints" in analysis["issues_detected"]:
            return "Price sensitivity detected. Consider targeted discount for switchers."
        if analysis["opportunities"]:
            return f"Opportunity: {analysis['opportunities'][0]}"
        return "Monitor sentiment. Prepare response strategies."

    async def analyze(self, competitor: str) -> Dict[str, Any]:
        mentions = await self.gather_social_mentions(competitor)
        analysis = self.analyze_sentiment(competitor, mentions)
        self.sentiment_history[competitor] = analysis
        return self.create_intelligence(competitor, analysis)


