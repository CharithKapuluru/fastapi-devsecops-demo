"""Configuration and logging setup."""

import logging
import sys
from typing import Any

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(name)s"}',
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


class Settings:
    """Application settings."""

    APP_NAME: str = "fastapi-devsecops-demo"
    VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    def dict(self) -> dict[str, Any]:
        """Return settings as dictionary."""
        return {
            "app_name": self.APP_NAME,
            "version": self.VERSION,
            "log_level": self.LOG_LEVEL,
        }


settings = Settings()
