import requests
from bs4 import BeautifulSoup
from loguru import logger
import asyncio
import websockets
import json
from tenacity import retry, stop_after_attempt, wait_exponential

class Scraper:
    def __init__(self):
        self.urls = []
        self.important_data_points = []

    def set_urls(self, urls):
        self.urls = urls

    @retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_data(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    async def scrape_async(self):
        results = {}
        for url in self.urls:
            try:
                html_content = self.fetch_data(url)
                results[url] = html_content
                logger.info(f"Fetched content from URL: {url}")
            except requests.RequestException as e:
                logger.error(f"Failed to retrieve content from URL: {url}, Error: {e}")
                results[url] = f"Failed to retrieve content, Error: {e}"
        return results

    async def focused_scraping(self):
        while True:
            results = {}
            for url in self.urls:
                try:
                    html_content = self.fetch_data(url)
                    soup = BeautifulSoup(html_content, 'html.parser')
                    data = {point: soup.select_one(point).text for point in self.important_data_points}
                    results[url] = data
                    async with websockets.connect("ws://localhost:6789") as websocket:
                        await websocket.send(json.dumps({"url": url, "data": data}))
                    logger.info(f"Fetched important data from URL: {url}")
                except requests.RequestException as e:
                    logger.error(f"Failed to retrieve content from URL: {url}, Error: {e}")
                    results[url] = f"Failed to retrieve content, Error: {e}"
            await asyncio.sleep(120)  # Rescrape every 2 minutes

    async def set_important_data_points(self, points):
        self.important_data_points = points

    async def websocket_listener(self):
        async with websockets.connect("ws://localhost:6789") as websocket:
            async for message in websocket:
                data = json.loads(message)
                if "important_data" in data:
                    await self.set_important_data_points(data["important_data"])
