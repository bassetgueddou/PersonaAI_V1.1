from pydantic_settings import BaseSettings
from typing import List
import os, json

class Settings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-4o-mini"
    log_level: str = "info"
    database_url: str
    allowed_origins: str = ""  # fuck u ruuuun brut

    class Config:
        env_file = ".env"

    @property
    def origins(self) -> List[str]:
        raw = self.allowed_origins
        if not raw:
            return []
        try:
            return json.loads(raw)
        except Exception:
            return [o.strip() for o in raw.split(",") if o.strip()]

settings = Settings()
