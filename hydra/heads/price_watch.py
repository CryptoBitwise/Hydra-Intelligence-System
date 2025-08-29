import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import re


from hydra.scrapers import scrape_intelligently


class PriceWatchHead:
    def __init__(self, brain=None):
        self.brain = brain
        self.name = "PriceWatch"
        self.monitoring = False
        self.price_history: Dict[str, Dict[str, Any]] = {}

    async def start_monitoring(self, competitors: List[str]):
        self.monitoring = True
        while self.monitoring:
            for competitor in competitors:
                try:
                    prices = await self.scrape_prices(competitor)
                    changes = self.detect_changes(competitor, prices)
                    if changes:
                        intel = self.create_intelligence(competitor, changes)
                        await self.brain.process_intelligence(intel)
                    self.price_history[competitor] = prices
                except Exception:
                    pass
                await asyncio.sleep(60)

    async def scrape_prices(self, competitor: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://{competitor}/products", headers={"User-Agent": "Mozilla/5.0"}
            )
            soup = BeautifulSoup(response.text, "html.parser")
            products: Dict[str, Any] = {}
            for item in soup.find_all("div", class_="product"):
                name = item.find("h3").text.strip()
                price_text = item.find("span", class_="price").text
                price = float(re.findall(r"[\d.]+", price_text)[0])
                products[name] = {
                    "price": price,
                    "currency": "USD",
                    "timestamp": datetime.now().isoformat(),
                    "in_stock": "out of stock" not in item.text.lower(),
                }
            return products

    def detect_changes(self, competitor: str, current_prices: Dict[str, Any]):
        if competitor not in self.price_history:
            return []
        changes = []
        old_prices = self.price_history[competitor]
        for product, current in current_prices.items():
            if product in old_prices:
                old = old_prices[product]
                if current["price"] != old["price"]:
                    change_pct = ((current["price"] - old["price"]) / old["price"]) * 100
                    changes.append(
                        {
                            "product": product,
                            "old_price": old["price"],
                            "new_price": current["price"],
                            "change_percent": change_pct,
                            "direction": "increased" if change_pct > 0 else "decreased",
                        }
                    )
        new_products = set(current_prices.keys()) - set(old_prices.keys())
        for product in new_products:
            changes.append({"type": "new_product", "product": product, "price": current_prices[product]["price"]})
        return changes

    def create_intelligence(self, competitor: str, changes: List[Dict[str, Any]]):
        max_change = max([abs(c.get("change_percent", 0)) for c in changes], default=0)
        if max_change > 20:
            threat = "critical"
        elif max_change > 10:
            threat = "high"
        elif max_change > 5:
            threat = "medium"
        else:
            threat = "low"
        discovery = f"Price changes detected: {len(changes)} items affected"
        if max_change > 0:
            discovery += f", max change: {max_change:.1f}%"
        return {
            "head": self.name,
            "competitor": competitor,
            "discovery": discovery,
            "threat_level": threat,
            "confidence": 0.95,
            "data": {"changes": changes},
        }

    def recommend_action(self, changes: List[Dict[str, Any]]) -> str:
        if any(c.get("change_percent", 0) < -15 for c in changes):
            return "URGENT: Competitor slashing prices. Consider matching or differentiate on value."
        if any(c.get("type") == "new_product" for c in changes):
            return "New competitor product detected. Analyze features and positioning."
        return "Monitor situation. No immediate action required."

    async def analyze(self, competitor: str) -> Dict[str, Any]:
        # Try Bright Data first (while we have credits); falls back automatically
        data = await scrape_intelligently(f"https://{competitor}/pricing")
        
        if data.get("source") == "bright_data":
            print(f"💰 Used Bright Data (credits remaining: ${250 - data.get('credits_used', 0):.2f})")
        else:
            print("🆓 Used free scraping")
        
        return {
            "head": self.name,
            "competitor": competitor,
            "discovery": f"Scraped via {data.get('source', 'unknown')}",
            "data": data,
        }


