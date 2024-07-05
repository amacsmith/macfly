import asyncio
import websockets
import json
from scraping.scraper import Scraper
from ai_integration.ai_regenerator import AIRegenerator

async def websocket_handler(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        url = data.get("url")
        if url:
            scraper = Scraper()
            scraper.set_urls([url])
            scraped_data = await scraper.scrape_async()
            from ai_integration.ai_regenerator import AIRegenerator
            ai_regen = AIRegenerator(model="openai", model_name="davinci")
            important_data = ai_regen.identify_important_data(scraped_data)
            response = {"important_data": important_data}
            await websocket.send(json.dumps(response))

start_server = websockets.serve(websocket_handler, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
