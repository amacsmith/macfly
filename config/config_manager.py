import os
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    def get_api_host(self):
        return os.getenv("API_HOST", "0.0.0.0")

    def get_api_port(self):
        return int(os.getenv("API_PORT", 8000))

    def get_api_user(self):
        return os.getenv("API_USER", "admin")

    def get_api_password(self):
        return os.getenv("API_PASSWORD", "password")

    def get_openai_api_key(self):
        return os.getenv("OPENAI_API_KEY")
