import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Dict, Any, List
import random
import re

class FreeScraper:
    """
    FREE web scraping - no Bright Data needed!
    This is what we'll use after the $250 credits run out.
    """
    
    def __init__(self):
        # Rotate user agents to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]
        
        self.timeout = 30
    
    def get_headers(self) -> Dict[str, str]:
        """Random headers to avoid detection"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    async def scrape(self, url: str) -> Dict[str, Any]:
        """
        Smart scraping with multiple fallback methods
        """
        methods = [
            ("direct", self.scrape_direct),
            ("playwright", self.scrape_with_playwright),
            ("requests_html", self.scrape_with_requests_html),
            ("archive", self.scrape_via_archive),
            ("google_cache", self.scrape_via_google_cache)
        ]
        
        for method_name, method in methods:
            try:
                print(f"🔍 Trying {method_name} for {url}")
                result = await method(url)
                if result and not result.get("error"):
                    result["method"] = method_name
                    result["source"] = "free_scraper"
                    return result
            except Exception as e:
                print(f"⚠️ {method_name} failed: {e}")
                continue
        
        return {
            "error": "All methods failed",
            "url": url,
            "source": "free_scraper"
        }
    
    async def scrape_direct(self, url: str) -> Dict[str, Any]:
        """Direct HTTP request - fastest method"""
        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            headers=self.get_headers()
        ) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract useful data
            data = {
                "url": url,
                "status_code": response.status_code,
                "title": soup.title.string if soup.title else "",
                "html": response.text[:50000],  # First 50k chars
                "headers": dict(response.headers),
            }
            
            # Extract specific data based on URL
            if "pricing" in url.lower():
                data["prices"] = self.extract_prices(soup)
            if "jobs" in url.lower() or "careers" in url.lower():
                data["jobs"] = self.extract_jobs(soup)
            if "about" in url.lower():
                data["tech_stack"] = self.extract_tech_stack(response.text)
            
            return data
    
    async def scrape_with_playwright(self, url: str) -> Dict[str, Any]:
        """For JavaScript-heavy sites"""
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                # Use chromium in headless mode
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                
                context = await browser.new_context(
                    user_agent=random.choice(self.user_agents)
                )
                
                page = await context.new_page()
                
                # Navigate and wait for content
                await page.goto(url, wait_until='networkidle')
                await page.wait_for_load_state('domcontentloaded')
                
                # Get content
                content = await page.content()
                title = await page.title()
                
                # Take screenshot for debugging
                # screenshot = await page.screenshot()
                
                await browser.close()
                
                soup = BeautifulSoup(content, 'html.parser')
                
                return {
                    "url": url,
                    "title": title,
                    "html": content[:50000],
                    "prices": self.extract_prices(soup) if "pricing" in url.lower() else [],
                    "jobs": self.extract_jobs(soup) if "jobs" in url.lower() else []
                }
                
        except ImportError:
            return {"error": "Playwright not installed"}
        except Exception as e:
            return {"error": f"Playwright error: {e}"}
    
    async def scrape_with_requests_html(self, url: str) -> Dict[str, Any]:
        """Alternative JS rendering"""
        try:
            from requests_html import AsyncHTMLSession
            
            session = AsyncHTMLSession()
            r = await session.get(url, headers=self.get_headers())
            await r.html.arender(timeout=20)
            
            return {
                "url": url,
                "title": r.html.find('title', first=True).text if r.html.find('title') else "",
                "html": r.html.html[:50000]
            }
            
        except ImportError:
            return {"error": "requests-html not installed"}
        except Exception as e:
            return {"error": f"requests-html error: {e}"}
    
    async def scrape_via_archive(self, url: str) -> Dict[str, Any]:
        """Use Archive.org as fallback"""
        archive_api = f"http://archive.org/wayback/available?url={url}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(archive_api)
            data = response.json()
            
            if data.get('archived_snapshots', {}).get('closest', {}).get('url'):
                snapshot_url = data['archived_snapshots']['closest']['url']
                return await self.scrape_direct(snapshot_url)
        
        return {"error": "No archive found"}
    
    async def scrape_via_google_cache(self, url: str) -> Dict[str, Any]:
        """Use Google's cache"""
        cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}"
        return await self.scrape_direct(cache_url)
    
    def extract_prices(self, soup: BeautifulSoup) -> List[float]:
        """Extract prices from HTML"""
        prices = []
        
        # Common price patterns
        price_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:USD|usd|\$)',
            r'(?:price|cost|fee)[:\s]+\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        ]
        
        text = soup.get_text()
        
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Clean and convert to float
                    price = float(match.replace(',', ''))
                    if 0 < price < 1000000:  # Reasonable price range
                        prices.append(price)
                except:
                    continue
        
        # Also check specific elements
        for element in soup.find_all(['span', 'div', 'p'], class_=re.compile(r'price|cost|fee', re.I)):
            text = element.get_text()
            for pattern in price_patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    try:
                        price = float(match.replace(',', ''))
                        if 0 < price < 1000000:
                            prices.append(price)
                    except:
                        continue
        
        return list(set(prices))  # Remove duplicates
    
    def extract_jobs(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract job postings"""
        jobs = []
        
        # Look for job listings
        job_elements = soup.find_all(['div', 'li', 'article'], 
                                    class_=re.compile(r'job|position|career|opening', re.I))
        
        for element in job_elements[:20]:  # Limit to 20
            job = {
                "title": "",
                "department": "",
                "location": ""
            }
            
            # Try to find title
            title = element.find(['h2', 'h3', 'h4', 'a'])
            if title:
                job["title"] = title.get_text().strip()
            
            # Try to find location
            location = element.find(text=re.compile(r'location|city|remote', re.I))
            if location:
                job["location"] = location.strip()
            
            if job["title"]:
                jobs.append(job)
        
        return jobs
    
    def extract_tech_stack(self, html: str) -> List[str]:
        """Extract technology mentions"""
        tech_keywords = [
            'react', 'angular', 'vue', 'javascript', 'python', 'java', 'ruby',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'postgresql', 'mongodb',
            'redis', 'elasticsearch', 'kafka', 'rabbitmq', 'graphql', 'rest api',
            'machine learning', 'artificial intelligence', 'blockchain', 'nodejs'
        ]
        
        tech_found = []
        html_lower = html.lower()
        
        for tech in html_lower.split():
            pass
        
        for tech in tech_keywords:
            if tech in html_lower:
                tech_found.append(tech)
        
        return tech_found
