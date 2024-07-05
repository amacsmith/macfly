import streamlit as st
import requests
import json
from requests.auth import HTTPBasicAuth
import time
import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_manager import ConfigManager

config = ConfigManager()
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Web Scraping Dashboard", layout="wide")

# Sidebar
st.sidebar.title("Configuration")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 60, 10)
ai_model = st.sidebar.selectbox("Select AI Model", ["openai", "anthropic", "claude_opus", "sonnet"])
urls = st.sidebar.text_area("Enter URLs (one per line)").splitlines()
prompt = st.sidebar.text_area("Enter Prompt (optional)")

# Main Content
st.title("Web Scraping Dashboard")

timeline = st.empty()

def log_to_timeline(message):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    timeline.markdown(f"{current_time} - {message}")

def initiate_scraping():
    scraping_request = {"urls": urls}
    auth = HTTPBasicAuth("admin", "password")
    response = requests.post(f"{API_URL}/api/start_scraping", json=scraping_request, auth=auth)
    log_to_timeline("Started scraping.")
    return response.json()

def parse_html():
    scraping_request = {"urls": urls}
    auth = HTTPBasicAuth("admin", "password")
    response = requests.post(f"{API_URL}/api/parse_html", json=scraping_request, auth=auth)
    log_to_timeline("Parsing HTML content.")
    return response.json()

def regenerate_content(data):
    regeneration_request = {
        "data": data,
        "api_key": config.get_openai_api_key(),
        "model": ai_model,
        "prompt": prompt
    }
    auth = HTTPBasicAuth("admin", "password")
    response = requests.post(f"{API_URL}/api/regenerate", json=regeneration_request, auth=auth)
    log_to_timeline("Regenerating content.")
    return response.json()

if st.button("Start Scraping"):
    scraping_result = initiate_scraping()
    st.json(scraping_result)
    log_to_timeline(f"Scraping result: {scraping_result}")

if st.button("Regenerate Content"):
    parsed_html = parse_html()
    if "data" in parsed_html:
        regenerated_content = regenerate_content(parsed_html["data"])
        st.json(regenerated_content)
        log_to_timeline(f"Regenerated content: {regenerated_content}")
    else:
        st.error("Failed to parse HTML.")
        log_to_timeline("Failed to parse HTML.")
