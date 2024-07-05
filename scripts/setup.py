import os
from dotenv import load_dotenv, set_key, find_dotenv

# Load existing .env file if it exists
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Define the environment variables you want to set
env_vars = {
    "OPENAI_API_KEY": "your_openai_api_key_here"
    # Add other environment variables as needed
}

# Update .env file only if variables do not already exist
for key, value in env_vars.items():
    if os.getenv(key) is None:
        set_key(dotenv_path, key, value)
        print(f"Setting {key} in .env file")
    else:
        print(f"{key} already set in .env file")

print("Environment setup complete.")
