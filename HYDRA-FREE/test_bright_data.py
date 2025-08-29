import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
from hydra.scrapers.bright_data import BrightDataScraper


async def test_bright_data():
    print("🧪 Testing Bright Data Connection...\n")
    
    if not os.getenv("BRIGHT_DATA_CUSTOMER_ID") and not os.getenv("BRIGHT_DATA_API_TOKEN"):
        print("❌ No Bright Data credentials found!")
        print("\nSet one of these:")
        print("1. BRIGHT_DATA_CUSTOMER_ID + BRIGHT_DATA_PASSWORD")
        print("2. BRIGHT_DATA_API_TOKEN")
        return
    
    scraper = BrightDataScraper()
    
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com",
    ]
    
    for url in test_urls:
        print(f"\n🔍 Testing: {url}")
        result = await scraper.scrape(url)
        
        if result.get("success"):
            print(f"✅ SUCCESS via {result['source']}")
            print(f"   Credits used: ${result['credits_used']:.3f}")
            print(f"   HTML length: {len(result.get('html', ''))}")
        else:
            print(f"❌ FAILED: {result.get('error')}")
            if result.get("fallback") == "free":
                print("   Will use free scraping as fallback")
    
    balance = await scraper.get_balance()
    if balance:
        print(f"\n💰 Account balance: ${balance}")
    
    print(f"\n📊 Total credits used in test: ${scraper.credits_used:.3f}")
    print(f"   Remaining from $250: ${250 - scraper.credits_used:.2f}")


if __name__ == "__main__":
    asyncio.run(test_bright_data())


