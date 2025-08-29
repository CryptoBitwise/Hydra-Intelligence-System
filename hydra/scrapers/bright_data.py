import os
import httpx
from typing import Dict, Any, Optional
import asyncio
import base64

class BrightDataScraper:
    """
    Bright Data scraper - using Web Scraper API (simpler than collectors)
    """
    
    def __init__(self):
        # Method 1: Web Scraper API (RECOMMENDED)
        self.customer_id = os.getenv("BRIGHT_DATA_CUSTOMER_ID", "")
        self.password = os.getenv("BRIGHT_DATA_PASSWORD", "")
        self.zone = os.getenv("BRIGHT_DATA_ZONE", "datacenter")
        
        # Method 2: Data Collector API Token
        self.api_token = os.getenv("BRIGHT_DATA_API_TOKEN", "")
        
        # Proxy URL for Web Scraper
        if self.customer_id and self.password:
            self.proxy_url = f"http://{self.customer_id}-zone-{self.zone}:{self.password}@zproxy.lum-superproxy.io:22225"
            self.method = "proxy"
            print("✅ Bright Data configured with Web Scraper API")
        elif self.api_token:
            self.api_url = "https://api.brightdata.com/dca/datasets"
            self.method = "api"
            print("✅ Bright Data configured with Data Collector API")
        else:
            self.method = None
            print("⚠️ No Bright Data credentials found")
        
        self.credits_used = 0
        self.credits_limit = 250
    
    async def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape using Bright Data
        """
        if not self.method:
            return {"error": "No Bright Data credentials", "fallback": "free"}
        
        # Check credits
        if self.credits_used >= self.credits_limit * 0.9:
            print(f"⚠️ Bright Data credits low: ${self.credits_used:.2f} used")
            return {"error": "Credits low", "fallback": "free"}
        
        try:
            if self.method == "proxy":
                return await self.scrape_via_proxy(url)
            else:
                return await self.scrape_via_api(url)
                
        except Exception as e:
            print(f"❌ Bright Data error: {e}")
            return {"error": str(e), "fallback": "free"}
    
    async def scrape_via_proxy(self, url: str) -> Dict[str, Any]:
        """
        Method 1: Use Bright Data as a proxy (EASIEST)
        """
        print(f"🔍 Scraping {url} via Bright Data proxy...")
        
        # Configure proxy
        proxies = {
            "http://": self.proxy_url,
            "https://": self.proxy_url
        }
        
        async with httpx.AsyncClient(proxies=proxies, timeout=30) as client:
            try:
                response = await client.get(url, follow_redirects=True)
                
                # Estimate credit usage
                self.credits_used += 0.001  # Roughly $0.001 per request
                
                return {
                    "url": url,
                    "status_code": response.status_code,
                    "html": response.text[:50000],  # First 50k chars
                    "headers": dict(response.headers),
                    "source": "bright_data_proxy",
                    "credits_used": self.credits_used,
                    "success": True
                }
                
            except Exception as e:
                print(f"Proxy error: {e}")
                return {"error": str(e), "fallback": "free"}
    
    async def scrape_via_api(self, url: str) -> Dict[str, Any]:
        """
        Method 2: Use Data Collector API
        """
        print(f"🔍 Scraping {url} via Bright Data API...")
        
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        # Simple web scraper request
        payload = {
            "url": url,
            "format": "json",
            "include_headers": True
        }
        
        async with httpx.AsyncClient(timeout=60) as client:
            try:
                # Start scraping job
                response = await client.post(
                    f"{self.api_url}/trigger",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code != 200:
                    return {"error": f"API error: {response.status_code}", "fallback": "free"}
                
                job_data = response.json()
                job_id = job_data.get("response_id") or job_data.get("id")
                
                if not job_id:
                    return {"error": "No job ID received", "fallback": "free"}
                
                # Poll for results
                for attempt in range(30):
                    await asyncio.sleep(2)
                    
                    result_response = await client.get(
                        f"{self.api_url}/get/{job_id}",
                        headers=headers
                    )
                    
                    if result_response.status_code == 200:
                        result = result_response.json()
                        
                        # Estimate credit usage
                        self.credits_used += 0.01
                        
                        return {
                            "url": url,
                            "data": result,
                            "source": "bright_data_api",
                            "credits_used": self.credits_used,
                            "success": True
                        }
                
                return {"error": "Timeout waiting for results", "fallback": "free"}
                
            except Exception as e:
                print(f"API error: {e}")
                return {"error": str(e), "fallback": "free"}
    
    async def get_balance(self) -> Optional[float]:
        """
        Check remaining balance (if API supports it)
        """
        if not self.api_token:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.brightdata.com/customer/balance",
                    headers={"Authorization": f"Bearer {self.api_token}"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("balance", 0)
        except:
            pass
        
        return None


class BrightDataScraper:
    """
    Bright Data scraper - use while we have $250 credits
    Then we'll switch to free methods
    """
    
    def __init__(self):
        self.api_key = os.getenv("BRIGHT_DATA_KEY", "")
        self.base_url = "https://api.brightdata.com"
        
        # Track credit usage (estimate)
        self.credits_used = 0
        self.credits_limit = 250  # $250 free credits
        
        if not self.api_key:
            print("⚠️ No Bright Data key found, will use free scraping")
    
    async def scrape(self, url: str, collector_id: str = "universal") -> Dict[str, Any]:
        """
        Scrape using Bright Data collector
        """
        if not self.api_key:
            return {"error": "No API key", "fallback": "free"}
        
        # Check if we're near credit limit
        if self.credits_used >= self.credits_limit * 0.9:  # 90% used
            print(f"⚠️ Bright Data credits running low: ${self.credits_used:.2f} used")
            return {"error": "Credits low", "fallback": "free"}
        
        try:
            result = await self.run_collector(collector_id, {"url": url})
            
            # Estimate credit usage (rough estimate)
            self.credits_used += 0.01  # Assume $0.01 per request
            
            return result
            
        except Exception as e:
            print(f"❌ Bright Data error: {e}")
            return {"error": str(e), "fallback": "free"}
    
    async def run_collector(self, collector_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Your Cursor-provided code - it's good!
        """
        if not self.api_key:
            return {"error": "BRIGHT_DATA_KEY missing"}
        
        base = f"{self.base_url}/collector"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=60) as client:
            # Start a collection
            r = await client.post(
                f"{base}/{collector_id}/start", 
                headers=headers, 
                json=params
            )
            r.raise_for_status()
            
            job_id = r.json().get("id")
            if not job_id:
                return {"error": "No job id", "resp": r.text}
            
            # Poll for results
            for attempt in range(30):
                await asyncio.sleep(2)  # Wait 2 seconds between polls
                
                s = await client.get(
                    f"{base}/results",
                    params={"collector_id": collector_id, "id": job_id},
                    headers=headers
                )
                
                if s.status_code == 200:
                    results = s.json()
                    if results:
                        return {
                            "job_id": job_id,
                            "results": results,
                            "source": "bright_data",
                            "credits_used": self.credits_used
                        }
            
            return {"error": "Timeout waiting for results", "job_id": job_id}
    
    async def get_credit_balance(self) -> Optional[float]:
        """
        Check remaining credits (if API supports it)
        """
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(
                    f"{self.base_url}/account/balance",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                if r.status_code == 200:
                    return r.json().get("balance", 0)
        except:
            pass
        
        return None
    
    async def scrape_prices(self, url: str) -> Dict[str, Any]:
        """
        Specialized price scraping
        """
        return await self.run_collector("e_commerce", {
            "url": url,
            "extract": ["prices", "products", "currency"]
        })
    
    async def scrape_jobs(self, company: str) -> Dict[str, Any]:
        """
        Specialized job scraping
        """
        return await self.run_collector("jobs", {
            "company": company,
            "sites": ["linkedin", "indeed", "glassdoor"]
        })

