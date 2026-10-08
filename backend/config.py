"""Application settings loaded from environment variables."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


load_dotenv()


class Settings(BaseModel):
    """
    Application configuration loaded from environment variables.
    """

    app_name: str = "LegalEase"
    app_version: str = "1.0.0"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    demo_mode: bool = False

    backend_url: str = "http://127.0.0.1:8000"

    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:8501",
            "http://127.0.0.1:8501",
        ]
    )

    ai_temperature: float = Field(
        default=0.35,
        ge=0.0,
        le=2.0,
    )

    ai_max_output_tokens: int = Field(
        default=8192,
        ge=256,
        le=32768,
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        """Parse comma-separated origins into a list."""
        if isinstance(value, str):
            return [
                item.strip()
                for item in value.split(",")
                if item.strip()
            ]

        return value


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.
    """

    return Settings(
        app_name=os.getenv(
            "APP_NAME",
            "LegalEase",
        ),
        app_version=os.getenv(
            "APP_VERSION",
            "1.0.0",
        ),
        gemini_api_key=os.getenv(
            "GEMINI_API_KEY",
            "",
        ),
        gemini_model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        ),
        demo_mode=os.getenv(
            "DEMO_MODE",
            "false",
        ).lower()
        == "true",
        backend_url=os.getenv(
            "BACKEND_URL",
            "http://127.0.0.1:8000",
        ),
        cors_origins=os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501",
        ),
        ai_temperature=float(
            os.getenv(
                "AI_TEMPERATURE",
                "0.35",
            )
        ),
        ai_max_output_tokens=int(
            os.getenv(
                "AI_MAX_OUTPUT_TOKENS",
                "8192",
            )
        ),
    )
