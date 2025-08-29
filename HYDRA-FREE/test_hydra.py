import asyncio
import os
from pathlib import Path
import json
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_test(name, status):
    icon = "✅" if status else "❌"
    color = Colors.GREEN if status else Colors.RED
    print(f"{color}{icon} {name}{Colors.END}")


async def test_hydra():
    print(f"""
    {Colors.BLUE}{Colors.BOLD}
    ╔════════════════════════════════════════════════╗
    ║              🐉 HYDRA TEST SUITE               ║
    ╚════════════════════════════════════════════════╝
    {Colors.END}
    """)

    # Test 1: Check file structure
    print(f"\n{Colors.BOLD}📁 Testing File Structure:{Colors.END}")
    required_files = [
        "hydra.py",
        "config.yaml",
        "requirements.txt",
        "hydra/__init__.py",
        "hydra/scrapers/free_scraper.py",
        "hydra/scrapers/bright_data.py",
        ".github/workflows/hydra.yml",
    ]
    for file in required_files:
        exists = Path(file).exists()
        print_test(f"  {file}", exists)

    # Test 2: Test imports
    print(f"\n{Colors.BOLD}📦 Testing Imports:{Colors.END}")
    try:
        import click  # noqa: F401
        print_test("  click", True)
    except Exception:
        print_test("  click", False)
    try:
        import httpx  # noqa: F401
        print_test("  httpx", True)
    except Exception:
        print_test("  httpx", False)
    try:
        from bs4 import BeautifulSoup  # noqa: F401
        print_test("  beautifulsoup4", True)
    except Exception:
        print_test("  beautifulsoup4", False)

    # Test 3: Test database
    print(f"\n{Colors.BOLD}💾 Testing Database:{Colors.END}")
    try:
        from hydra import HydraFree
        hydra = HydraFree()
        print_test("  Database initialized", True)

        test_intel = {
            "head": "TEST",
            "competitor": "test.com",
            "discovery": "Test discovery",
            "threat_level": "low",
            "confidence": 0.5,
            "data": {"test": True},
        }
        hydra.save_intelligence(test_intel)
        print_test("  Save intelligence", True)

        recent = hydra.get_recent_intelligence(1)
        print_test("  Retrieve intelligence", len(recent) > 0)
    except Exception as e:
        print_test(f"  Database error: {e}", False)

    # Test 4: Test scrapers
    print(f"\n{Colors.BOLD}🕷️ Testing Scrapers:{Colors.END}")
    try:
        from hydra.scrapers.free_scraper import FreeScraper
        scraper = FreeScraper()
        result = await scraper.scrape("https://example.com")
        print_test("  Free scraper", not result.get("error"))
    except Exception as e:
        print_test(f"  Free scraper error: {e}", False)

    if os.getenv("BRIGHT_DATA_KEY"):
        try:
            from hydra.scrapers.bright_data import BrightDataScraper
            bd_scraper = BrightDataScraper()
            print_test("  Bright Data configured", True)
            print(f"    {Colors.YELLOW}Credits: ${250 - bd_scraper.credits_used:.2f} remaining{Colors.END}")
        except Exception:
            print_test("  Bright Data", False)
    else:
        print(f"  {Colors.YELLOW}⚠️  No Bright Data key (will use free scraping){Colors.END}")

    # Test 5: Test heads import
    print(f"\n{Colors.BOLD}🐉 Testing HYDRA Heads:{Colors.END}")
    heads_to_test = ["price_watch", "job_spy", "tech_radar"]
    for mod in heads_to_test:
        try:
            __import__(f"hydra.heads.{mod}")
            print_test(f"  {mod}", True)
        except Exception:
            print_test(f"  {mod}", False)

    # Test 6: Test orchestrated scrape
    print(f"\n{Colors.BOLD}🔍 Testing Orchestrated Scrape:{Colors.END}")
    try:
        from hydra.scrapers import scrape_intelligently
        data = await scrape_intelligently("https://example.com/pricing")
        print_test("  scrape_intelligently", not data.get("error"))
    except Exception as e:
        print_test(f"  scrape_intelligently error: {e}", False)

    # Test 7: Workflow presence
    print(f"\n{Colors.BOLD}⚙️ Testing GitHub Actions:{Colors.END}")
    workflow_path = Path(".github/workflows/hydra.yml")
    if workflow_path.exists():
        print_test("  Workflow file exists", True)
        with open(workflow_path, encoding='utf-8') as f:
            content = f.read()
            print_test("  Schedule configured", "schedule:" in content)
            print_test("  Collect job defined", "collect-intelligence:" in content)
    else:
        print_test("  Workflow file", False)

    # Test 8: Dashboard
    print(f"\n{Colors.BOLD}🌐 Testing Dashboard:{Colors.END}")
    dashboard_path = Path("dashboard/index.html")
    print_test("  Dashboard HTML", dashboard_path.exists())

    print(f"""
    {Colors.BOLD}
    ════════════════════════════════════════════════
    {Colors.GREEN}🎉 HYDRA Test Complete!{Colors.END}
    {Colors.BOLD}════════════════════════════════════════════════
    {Colors.END}
    """)


if __name__ == "__main__":
    import sys
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Python 3.8+ required{Colors.END}")
        raise SystemExit(1)
    asyncio.run(test_hydra())


