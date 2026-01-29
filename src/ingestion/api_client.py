# Import libraries
import time
from typing import Any, Optional

import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)


class APIClient:
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def fetch(
        self, url: str, params: Optional[dict[str, Any]] = None
    ) -> dict[str, Any]:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise
        raise RuntimeError("Max retries exceeded")
