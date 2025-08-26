import httpx
import asyncio
import json

async def test_hydra_api():
    """Test HYDRA API endpoints"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Test root endpoint
        response = await client.get(f"{base_url}/")
        print("Root:", response.json())
        
        # Test health check
        response = await client.get(f"{base_url}/health")
        print("Health:", response.json())
        
        # Get competitors
        response = await client.get(f"{base_url}/api/competitors")
        print("Competitors:", response.json())
        
        # Get head status
        response = await client.get(f"{base_url}/api/heads")
        print("Heads:", response.json())
        
        # Create test intelligence
        test_intel = {
            "head": "PriceWatch",
            "competitor": "competitor1.com",
            "discovery": "Price dropped 25% on flagship product",
            "threat_level": "high",
            "confidence": 0.95,
            "data": {"price_change": -25, "product": "Product X"},
            "recommended_action": "Consider price matching or value differentiation"
        }
        
        response = await client.post(
            f"{base_url}/api/intelligence",
            json=test_intel
        )
        print("Created Intelligence:", response.json())
        
        # Get dashboard stats
        response = await client.get(f"{base_url}/api/dashboard/stats")
        print("Dashboard Stats:", response.json())

if __name__ == "__main__":
    asyncio.run(test_hydra_api())
