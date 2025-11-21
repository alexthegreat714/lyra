"""
Lyra Agent Configuration

Loads environment variables and defines core settings for the Lyra agent.
"""

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel


# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    """Core settings for the Lyra agent."""

    # Agent identity
    AGENT_NAME: str = "Lyra"
    VERSION: str = "0.1"

    # Server settings
    HOST: str = os.getenv("LYRA_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("LYRA_PORT", "8000"))
    DEBUG: bool = os.getenv("LYRA_DEBUG", "false").lower() == "true"

    # Base paths
    BASE_DIR: Path = Path(__file__).parent

    # Memory paths
    MEMORY_DIR: Path = BASE_DIR / "memory"
    SHORT_TERM_MEMORY_DIR: Path = MEMORY_DIR / "short_term"
    LONG_TERM_MEMORY_DIR: Path = MEMORY_DIR / "long_term"

    # RAG paths
    RAG_DIR: Path = BASE_DIR / "rag"

    # Logs path
    LOGS_DIR: Path = BASE_DIR / "logs"

    class Config:
        arbitrary_types_allowed = True


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: The application settings
    """
    return Settings()
