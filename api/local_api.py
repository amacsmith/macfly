import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from scraping.scraper import Scraper
from ai_integration.ai_regenerator import AIRegenerator
from ai_integration.openai import OpenAIHTMLParser
from config.config_manager import ConfigManager
from loguru import logger
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

config = ConfigManager()

app = FastAPI()
scraper = Scraper()
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != config.get_api_user() or credentials.password != config.get_api_password():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

class RegenerationRequest(BaseModel):
    data: dict
    api_key: str
    model: str

class ScrapingRequest(BaseModel):
    urls: list
    prompt: str = None

@app.get("/api/data")
async def get_data(credentials: HTTPBasicCredentials = Depends(authenticate)):
    data = await scraper.scrape_async()
    logger.info("Data fetched successfully")
    return data

@app.post("/api/start_scraping")
async def start_scraping(request: ScrapingRequest, credentials: HTTPBasicCredentials = Depends(authenticate)):
    scraper.set_urls(request.urls)
    asyncio.create_task(scraper.focused_scraping())
    return {"status": "scraping started"}

@app.post("/api/parse_html")
async def parse_html(request: ScrapingRequest, credentials: HTTPBasicCredentials = Depends(authenticate)):
    scraper.set_urls(request.urls)
    html_data = await scraper.scrape_async()
    
    parser = OpenAIHTMLParser(api_key=config.get_openai_api_key(), model="gpt-4")  # Use your preferred model
    parsed_data = {}
    for url, html in html_data.items():
        await AIRegenerator(api_key=config.get_openai_api_key(), model="openai").analyze_and_notify(html, request.prompt)
        parsed_data[url] = parser.parse(html, request.prompt)
    return {"status": "html parsed", "data": parsed_data}

@app.post("/api/regenerate")
async def regenerate_content(request: RegenerationRequest, credentials: HTTPBasicCredentials = Depends(authenticate)):
    regenerator = AIRegenerator(api_key=request.api_key, model=request.model)
    regenerated_content = regenerator.generate_site(request.data)
    return {"regenerated_content": regenerated_content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.get_api_host(), port=config.get_api_port(), log_level="info")
