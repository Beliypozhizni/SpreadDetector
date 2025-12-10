import asyncio
import logging
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


class HttpClient:
    """Universal HTTP client for all exchanges"""

    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self.request_count = 0

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def get_json(self, endpoint: str, **kwargs) -> Optional[dict]:
        """GET request returning JSON"""
        url = f"https://{self.base_url}{endpoint}"
        self.request_count += 1

        try:
            async with self.session.get(url, **kwargs) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None

                # Можно добавить проверку content-type
                content_type = response.headers.get('content-type', '')
                if 'application/json' not in content_type:
                    logger.error(f"Non-JSON response from {url}: {content_type}")
                    return None

                return await response.json()

        except aiohttp.ClientError as e:
            logger.error(f"Network error {url}: {e}")
            return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout {url}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error {url}: {e}", exc_info=True)
            return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
