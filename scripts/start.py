import os
import subprocess
import sys
import threading
from config.config_manager import ConfigManager
import time

config = ConfigManager()

def start_websocket_server():
    subprocess.Popen([sys.executable, "scripts/websocket_server.py"])

def start_api():
    subprocess.Popen([sys.executable, "scripts/start_api.py"])

def start_interface():
    subprocess.Popen([sys.executable, "scripts/start_interface.py"])

if __name__ == "__main__":
    # Start the WebSocket server
    websocket_thread = threading.Thread(target=start_websocket_server)
    websocket_thread.start()

    # Give some time for WebSocket server to start
    time.sleep(5)

    # Start the API
    api_thread = threading.Thread(target=start_api)
    api_thread.start()

    # Start the Streamlit interface
    interface_thread = threading.Thread(target=start_interface)
    interface_thread.start()
    
    # Join threads
    websocket_thread.join()
    api_thread.join()
    interface_thread.join()
