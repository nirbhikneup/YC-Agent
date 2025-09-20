from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

app = FastAPI(title="YC Company Scraper API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to track scraping status
scraping_status = {
    "is_running": False,
    "progress": 0,
    "total": 0,
    "current_company": "",
    "batch": "",
    "start_time": None,
    "results": None,
    "error": None
}

class ScrapeRequest(BaseModel):
    batch: str

class ScrapeResponse(BaseModel):
    message: str
    batch: str
    task_id: str

@app.get("/")
async def root():
    return {"message": "YC Company Scraper API", "status": "running", "note": "This is a simplified version for Vercel deployment"}

@app.get("/status")
async def get_status():
    return scraping_status

@app.post("/scrape", response_model=ScrapeResponse)
async def start_scraping(request: ScrapeRequest, background_tasks: BackgroundTasks):
    if scraping_status["is_running"]:
        raise HTTPException(status_code=400, detail="Scraping is already in progress")
    
    # Reset status
    scraping_status.update({
        "is_running": True,
        "progress": 0,
        "total": 0,
        "current_company": "",
        "batch": request.batch,
        "start_time": datetime.now().isoformat(),
        "results": None,
        "error": None
    })
    
    # Start background task
    background_tasks.add_task(run_simple_scraper, request.batch)
    
    return ScrapeResponse(
        message="Scraping started (simplified version)",
        batch=request.batch,
        task_id="scrape_task"
    )

async def run_simple_scraper(batch: str):
    try:
        # This is a simplified version that doesn't use Playwright
        # For full functionality, use the local version with Playwright
        
        # Simulate scraping process
        companies = []
        for i in range(10):  # Simulate 10 companies
            await asyncio.sleep(1)  # Simulate delay
            companies.append({
                "name": f"Sample Company {i+1}",
                "link": f"https://example.com/company{i+1}",
                "batch": batch,
                "emails": f"contact{i+1}@example.com",
                "email_count": 1
            })
            
            scraping_status.update({
                "progress": i + 1,
                "total": 10,
                "current_company": f"Sample Company {i+1}"
            })
        
        # Update status with results
        scraping_status.update({
            "is_running": False,
            "results": {
                "total_companies": len(companies),
                "companies_with_emails": len(companies),
                "filename": f"yc_companies_{batch.replace(' ', '_')}.csv",
                "note": "This is sample data. For full scraping, use the local version."
            }
        })
        
        # Save results
        df = pd.DataFrame(companies)
        filename = f"yc_companies_{batch.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False)
        scraping_status["results"]["file_saved"] = True
        
    except Exception as e:
        scraping_status.update({
            "is_running": False,
            "error": str(e)
        })

@app.get("/download/{filename}")
async def download_file(filename: str):
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        filename,
        media_type='text/csv',
        filename=filename
    )

@app.get("/results")
async def get_results():
    if not scraping_status["results"]:
        raise HTTPException(status_code=404, detail="No results available")
    
    return scraping_status["results"]

@app.post("/reset")
async def reset_status():
    global scraping_status
    scraping_status = {
        "is_running": False,
        "progress": 0,
        "total": 0,
        "current_company": "",
        "batch": "",
        "start_time": None,
        "results": None,
        "error": None
    }
    return {"message": "Status reset"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
