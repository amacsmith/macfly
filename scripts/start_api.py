import os
import sys
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_manager import ConfigManager

config = ConfigManager()

if __name__ == "__main__":
    uvicorn.run("api.local_api:app", host=config.get_api_host(), port=config.get_api_port(), log_level="info")
