from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List
import httpx

router = APIRouter(
    prefix="/api/integrations",
    tags=["integrations"]
)

@router.post("/n8n/webhook")
async def n8n_webhook(payload: Dict[str, Any]):
    """Webhook endpoint for n8n workflows"""
    
    # Process n8n workflow data
    workflow_name = payload.get("workflow", "unknown")
    data = payload.get("data", {})
    
    # Route to appropriate handler based on workflow
    if workflow_name == "bright_data_collector":
        return await process_bright_data(data)
    elif workflow_name == "alert_trigger":
        return await process_alert(data)
    
    return {"status": "received", "workflow": workflow_name}

@router.post("/bright-data/process")
async def process_bright_data(data: Dict[str, Any]):
    """Process data from Bright Data collectors"""
    
    collector_type = data.get("collector_type")
    results = data.get("results", [])
    
    processed = []
    
    for result in results:
        # Process based on collector type
        if collector_type == "price_monitor":
            processed.append(process_price_data(result))
        elif collector_type == "job_boards":
            processed.append(process_job_data(result))
        # Add more processors
    
    return {"processed": len(processed), "data": processed}

def process_price_data(data: Dict) -> Dict:
    """Process price monitoring data"""
    return {
        "type": "price_change",
        "product": data.get("product_name"),
        "old_price": data.get("old_price"),
        "new_price": data.get("new_price"),
        "change_percent": calculate_percentage_change(
            data.get("old_price"), 
            data.get("new_price")
        )
    }

def process_job_data(data: Dict) -> Dict:
    """Process job posting data"""
    return {
        "type": "job_posting",
        "title": data.get("job_title"),
        "company": data.get("company"),
        "skills": data.get("required_skills", []),
        "posted_date": data.get("posted_date")
    }

def calculate_percentage_change(old: float, new: float) -> float:
    if old == 0 or old is None or new is None:
        return 0
    return ((new - old) / old) * 100

async def process_alert(data: Dict[str, Any]):
    # Placeholder for processing alert-specific workflows
    return {"status": "alert_processed", "data": data}
