import os
import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Load .env file if present
PROJECT_ROOT = Path(__file__).parent.parent
load_dotenv(PROJECT_ROOT / ".env")

class BackendSettings(BaseModel):
    database_url: str
    redis_host: str
    redis_port: int
    n_clusters: int
    num_people_refilter: int
    admin_password: str
    faiss_index_path: str
    embedding_dim: int
    cors_origins: List[str]

class BotSettings(BaseModel):
    token: str
    backend_url: str

class FrontendSettings(BaseModel):
    default_limit: int

class Settings(BaseModel):
    backend: BackendSettings
    bot: BotSettings
    frontend: FrontendSettings


def _override_from_env(settings: Settings) -> Settings:
    # Prefer environment values when present (e.g. .env or container env vars)
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
    if token:
        settings.bot.token = token

    # Optional overrides for backend settings via env vars
    if os.getenv("BACKEND_DATABASE_URL"):
        settings.backend.database_url = os.getenv("BACKEND_DATABASE_URL")
    if os.getenv("REDIS_HOST"):
        settings.backend.redis_host = os.getenv("REDIS_HOST")
    if os.getenv("REDIS_PORT"):
        settings.backend.redis_port = int(os.getenv("REDIS_PORT"))
    if os.getenv("ADMIN_PASSWORD"):
        settings.backend.admin_password = os.getenv("ADMIN_PASSWORD")

    return settings


def load_config():
    # Load from root directory (parent of backend)
    config_path = PROJECT_ROOT / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found at {config_path}. Make sure config.yaml exists in the project root."
        )
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)

    settings = Settings(**data)
    settings = _override_from_env(settings)

    if not settings.bot.token:
        raise ValueError(
            "Bot token is required. Please set TELEGRAM_BOT_TOKEN in .env or config.yaml."
        )

    return settings


settings = load_config()
