import os
import yaml
from pathlib import Path
from pydantic import BaseModel
from typing import List

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

def load_config():
    # Load from root directory
    config_path = Path(__file__).parent.parent / "config.yaml"
    with open(config_path, "r") as f:
        data = yaml.safe_load(f)
    return Settings(**data)

settings = load_config()