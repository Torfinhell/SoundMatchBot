import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# Load from root config.yaml
config_path = Path(__file__).parent.parent.parent / "config.yaml"
if not config_path.exists():
    raise FileNotFoundError(f"Config file not found at {config_path}. Make sure config.yaml exists in the project root.")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Prefer environment variable for token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or config['bot']['token']
BACKEND_URL = config['bot']['backend_url']