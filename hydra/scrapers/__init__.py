"""
HYDRA Scraping System
- Uses Bright Data while we have credits ($250 free)
- Falls back to free scraping when credits run out
- No vendor lock-in!
"""

import os
from typing import Dict, Any


async def scrape_intelligently(url: str, method: str = "auto") -> Dict[str, Any]:
    """
    Smart scraping that uses the best available method
    """

    # Check if we should use Bright Data
    if os.getenv("BRIGHT_DATA_KEY") and method != "free":
        try:
            from hydra.scrapers.bright_data import BrightDataScraper
            scraper = BrightDataScraper()
            result = await scraper.scrape(url)
            if result and not result.get("error"):
                print(f"✅ Scraped via Bright Data: {url}")
                return result
        except Exception as e:
            print(f"⚠️ Bright Data failed, using free scraping: {e}")

    # Fallback to free scraping
    from hydra.scrapers.free_scraper import FreeScraper
    scraper = FreeScraper()
    result = await scraper.scrape(url)
    print(f"✅ Scraped via free method: {url}")
    return result


