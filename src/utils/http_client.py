import aiohttp

from src.utils.logger import logger


class HttpClient:
    def __init__(self, base_url: str = "", timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_json(self, endpoint: str, **kwargs) -> dict | None:
        url = f"https://{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint

        try:
            async with self.session.get(url, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                logger.warning(f"GET {url} returned {response.status}")
        except Exception as e:
            logger.error(f"GET {url} failed: {e}")
        return None
