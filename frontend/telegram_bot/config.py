import yaml
from pathlib import Path

# Load from root config.yaml
config_path = Path(__file__).parent.parent.parent / "config.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

BOT_TOKEN = config['bot']['token']
BACKEND_URL = config['bot']['backend_url']