from typing import *
import aiohttp
import asyncio
from .types import Payload, OPCODES
import json
from .errors import DiscmojiRatelimit
import warnings
import logging

logger = logging.getLogger(__name__)

class EndpointManager:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://discord.com/api/v10"
        self.headers = {
            "User-Agent": "DiscordBot https://github.com/mojidev-py/discmoji, 0.0.1pr",
            "Authorization": f"Bot {token}",
        }
        self.httpclient = aiohttp.ClientSession(base_url=self.base_url, headers=self.headers)

    def ratelimited(self, request: aiohttp.ClientResponse):
        retry_after = request.headers.get("Retry-After")
        if retry_after and retry_after.isdigit() and int(retry_after) > 0:
            return (True, int(retry_after))
        return (False, 0)

    async def _send(self, method: str, route: str) -> Payload:
        try:
            async with self.httpclient as client:
                sent = await client.request(method, self.base_url + route)
                parsed = await sent.read()
                decoded = parsed.decode(encoding="utf-8")
                check, retry_after = self.ratelimited(sent)
                if check:
                    warnings.warn(DiscmojiRatelimit(f"{retry_after}"))
                return Payload(code=OPCODES.HTTP, d=json.loads(decoded), event_name="HTTP_REQUEST_RECEIVED")
        except aiohttp.ClientError as e:
            logger.error(f"HTTP request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    async def send_request(self, method: Literal['get', 'post', 'put', 'patch', 'delete'], route: str) -> Payload:
        return await self._send(method, route)
