from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List

class Settings(BaseSettings):
    openai_api_key: str = Field(alias="OPENAI_API_KEY")
    model_name: str = Field(default="gpt-4o-mini", alias="MODEL_NAME")
    log_level: str = Field(default="info", alias="LOG_LEVEL")
    allowed_origins: List[str] = Field(default_factory=lambda: ["http://localhost:5173"], alias="ALLOWED_ORIGINS")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    model_config = {"protected_namespaces": ("settings_",)}

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        # Fuck you accepte tout
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                import json
                return json.loads(s)
            return [x.strip() for x in s.split(",") if x.strip()]
        return v


settings = Settings()