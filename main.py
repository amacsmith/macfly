import subprocess
import os
from threading import Thread

def run_fastapi():
    subprocess.run(["python", "scripts/start_api.py"])

def run_streamlit():
    subprocess.run(["streamlit", "run", "dynamic_interface/app.py"])

def run_websocket_server():
    subprocess.run(["python", "scripts/websocket_server.py"])

if __name__ == "__main__":
    Thread(target=run_fastapi).start()
    Thread(target=run_streamlit).start()
    Thread(target=run_websocket_server).start()
