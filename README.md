# Web Scraping App

## Overview

This application scrapes data from open browser tabs, aggregates it into a local API, and displays the data in a dynamic interface for real-time updates and configuration. The aggregated data can also be used to regenerate web pages using AI models like Anthropic, OpenAI, Gemini, or Groq.

## Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/web_scraping_app.git
   cd web_scraping_app
   ```

2. **Run the Script:**

   ```sh
   bash scripts/setup.sh
   ```

3. **Configure your environment variables:**

    - Edit the `.env` file created from the `.env.example` template and add your API Keys and settings.

## Usage

1. **Start the FastAPI application:**

   ```sh
   bash scripts/start_api.sh
   ```

2. **Start the Streamlit interface:**

   ```sh
   bash scripts/start_interface.sh
   ```

3. Open your browser and navigate to <http://localhost:8501> to access the Streamlit interface.

## Testing

1. **Run the tests:**

   ```sh
   python -m unittest discover tests
   ```

## Logging

Logs are stored in `logs/scraper.log` with detailed information about scraping activities.

## Caching

A simple caching mechanism is implemented to avoid redundant data fetching, with a default TTL (Time to Live) of 300 seconds.

## Running the Project

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/amacsmith/macscrape.git
   ```

2. **Run the Setup Script:**

   ```sh
   bash scripts/setup.sh
   ```

3. **Configure Environment Variables:**

    - Edit the `.env` file and add your API keys and settings

4. **Start the FastAPI Application:**

   ```sh
   bash scripts/start_api.sh
   ```

5. **Start the Streamlit Interface:**

   ```sh
   bash scripts/start_interface.sh
   ```

6. **Access the Interface:**

    - Open your browser and navigate to <http://localhost:8501> to access the Streamlit interface.
    - Configure scraping parameters and view data in real-time.
    - Use AI integration to regenerate web pages based on scraped data.

    By following these steps, the setup and deployment process will be automated, making it easier to get the application running quickly.

## File and Folder Structure

```plaintext
macscrape/
├── ai_integration/
│   ├── __init__.py
│   ├── ai_regenerator.py
│   ├── openai.py
│   ├── anthropic.py
│   ├── claude_opus.py
│   ├── sonnet.py
├── api/
│   ├── __init__.py
│   ├── local_api.py
├── config/
│   ├── __init__.py
│   ├── config_manager.py
├── dynamic_interface/
│   ├── __init__.py
│   ├── app.py
│   ├── static/
│   ├── templates/
│   │   ├── __init__.py
│   │   ├── base.html
│   │   ├── index.html
├── logs/
│   ├── scraper.log
├── scraping/
│   ├── __init__.py
│   ├── scraper.py
│   ├── config_manager.py
├── scripts/
│   ├── __init__.py
│   ├── check_env.py
│   ├── setup.py
│   ├── start.py
│   ├── start_api.py
│   ├── start_interface.py
│   ├── websocket_server.py
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py
├── utils/
│   ├── __init__.py
│   ├── helpers.py
├── venv/
├── .env
├── .env.example
├── main.py
├── README.md
├── requirements.txt
```
