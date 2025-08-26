# backend/heads/price_watch.py - The Price Monitoring Head
import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class PriceWatchHead:
    """
    Monitors competitor pricing in real-time.
    Detects price changes, discounts, new products.
    """
    
    def __init__(self, brain):
        self.brain = brain
        self.name = "PriceWatch"
        self.monitoring = False
        self.price_history = {}
        logger.info(f"👁️ PriceWatch Head initialized")
        
    async def start_monitoring(self, competitors: List[str]):
        """Begin monitoring competitor prices"""
        self.monitoring = True
        logger.info(f"👁️ PriceWatch starting monitoring for {len(competitors)} competitors")
        
        while self.monitoring:
            for competitor in competitors:
                try:
                    # Check prices
                    prices = await self.scrape_prices(competitor)
                    
                    # Detect changes
                    changes = self.detect_changes(competitor, prices)
                    
                    if changes:
                        # Report to brain
                        intel = self.create_intelligence(competitor, changes)
                        await self.brain.process_intelligence(intel)
                    
                    # Update history
                    self.price_history[competitor] = prices
                    
                except Exception as e:
                    logger.error(f"❌ PriceWatch error for {competitor}: {e}")
                
                # Don't hammer servers
                await asyncio.sleep(60)
    
    async def scrape_prices(self, competitor: str) -> Dict[str, Any]:
        """Scrape current prices from competitor"""
        logger.info(f"👁️ Scraping prices from {competitor}")
        
        # This is where Bright Data shines
        config = self.get_bright_data_config(competitor)
        
        # For demo, using direct scraping
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://{competitor}/products",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products = {}
            for item in soup.find_all('div', class_='product'):
                name = item.find('h3').text.strip()
                price_text = item.find('span', class_='price').text
                price = float(re.findall(r'[\d.]+', price_text)[0])
                
                products[name] = {
                    'price': price,
                    'currency': 'USD',
                    'timestamp': datetime.now().isoformat(),
                    'in_stock': 'out of stock' not in item.text.lower()
                }
            
            logger.info(f"👁️ Scraped {len(products)} products from {competitor}")
            return products
    
    def detect_changes(self, competitor: str, current_prices: Dict) -> List[Dict]:
        """Detect price changes"""
        if competitor not in self.price_history:
            return []  # First scan, no changes yet
        
        changes = []
        old_prices = self.price_history[competitor]
        
        for product, current in current_prices.items():
            if product in old_prices:
                old = old_prices[product]
                if current['price'] != old['price']:
                    change_pct = ((current['price'] - old['price']) / old['price']) * 100
                    
                    changes.append({
                        'product': product,
                        'old_price': old['price'],
                        'new_price': current['price'],
                        'change_percent': change_pct,
                        'direction': 'increased' if change_pct > 0 else 'decreased'
                    })
        
        # Check for new products
        new_products = set(current_prices.keys()) - set(old_prices.keys())
        for product in new_products:
            changes.append({
                'type': 'new_product',
                'product': product,
                'price': current_prices[product]['price']
            })
        
        if changes:
            logger.info(f"👁️ Detected {len(changes)} changes for {competitor}")
        
        return changes
    
    def create_intelligence(self, competitor: str, changes: List[Dict]):
        """Create intelligence report for brain"""
        from backend.core.brain import Intelligence, ThreatLevel
        
        # Assess threat level
        max_change = max([abs(c.get('change_percent', 0)) for c in changes], default=0)
        
        if max_change > 20:
            threat = ThreatLevel.CRITICAL
        elif max_change > 10:
            threat = ThreatLevel.HIGH
        elif max_change > 5:
            threat = ThreatLevel.MEDIUM
        else:
            threat = ThreatLevel.LOW
        
        discovery = f"Price changes detected: {len(changes)} items affected"
        if max_change > 0:
            discovery += f", max change: {max_change:.1f}%"
        
        return Intelligence(
            head=self.name,
            competitor=competitor,
            discovery=discovery,
            threat_level=threat,
            confidence=0.95,
            timestamp=datetime.now(),
            data={'changes': changes},
            recommended_action=self.recommend_action(changes)
        )
    
    def recommend_action(self, changes: List[Dict]) -> str:
        """AI-powered action recommendation"""
        if any(c.get('change_percent', 0) < -15 for c in changes):
            return "URGENT: Competitor slashing prices. Consider matching or differentiate on value."
        elif any(c.get('type') == 'new_product' for c in changes):
            return "New competitor product detected. Analyze features and positioning."
        else:
            return "Monitor situation. No immediate action required."
    
    def get_bright_data_config(self, competitor: str):
        """Bright Data collector configuration"""
        return {
            "collector_id": "price_monitor",
            "target_url": f"https://{competitor}",
            "selectors": {
                "products": "div.product",
                "name": "h3",
                "price": "span.price",
                "stock": "span.availability"
            },
            "schedule": "*/5 * * * *"  # Every 5 minutes
        }
    
    async def deep_investigate(self, competitor: str, trigger: str):
        """Deep investigation when triggered by brain"""
        logger.info(f"👁️ PriceWatch deep investigating {competitor} due to: {trigger}")
        
        # More thorough price analysis
        prices = await self.scrape_prices(competitor)
        
        # Analyze pricing patterns
        analysis = self.analyze_pricing_patterns(prices)
        
        # Create detailed intelligence
        intel = Intelligence(
            head=self.name,
            competitor=competitor,
            discovery=f"Deep price analysis: {analysis['summary']}",
            threat_level=ThreatLevel.MEDIUM,
            confidence=0.9,
            timestamp=datetime.now(),
            data={'prices': prices, 'analysis': analysis},
            recommended_action="Continue monitoring pricing strategy"
        )
        
        await self.brain.process_intelligence(intel)
        return intel
    
    def analyze_pricing_patterns(self, prices: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze pricing patterns and strategies"""
        if not prices:
            return {"summary": "No pricing data available"}
        
        price_values = [p['price'] for p in prices.values()]
        
        return {
            "summary": f"Analyzed {len(prices)} products",
            "price_range": {
                "min": min(price_values),
                "max": max(price_values),
                "avg": sum(price_values) / len(price_values)
            },
            "pricing_strategy": self.determine_pricing_strategy(price_values),
            "competitive_position": "mid-market"  # Simplified for demo
        }
    
    def determine_pricing_strategy(self, prices: List[float]) -> str:
        """Determine competitor's pricing strategy"""
        if not prices:
            return "unknown"
        
        avg_price = sum(prices) / len(prices)
        price_variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
        
        if price_variance < 100:
            return "uniform pricing"
        elif avg_price > 1000:
            return "premium pricing"
        elif avg_price < 100:
            return "budget pricing"
        else:
            return "tiered pricing"
    
    async def stop(self):
        """Stop monitoring"""
        self.monitoring = False
        logger.info("👁️ PriceWatch monitoring stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "name": self.name,
            "monitoring": self.monitoring,
            "competitors_tracked": len(self.price_history),
            "total_products": sum(len(prices) for prices in self.price_history.values()),
            "last_scan": datetime.now().isoformat()
        }

# Create instance (will be attached to brain)
price_watch = PriceWatchHead(None)  # Brain will be set when attached
