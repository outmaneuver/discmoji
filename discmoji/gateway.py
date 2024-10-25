from typing import *
import aiohttp
import asyncio
from .types import Payload,OPCODES,initiatelogging,formatter,AppInfo
from random import uniform
import os
from ._http import EndpointManager
from .errors import DiscmojiAPIError


class GatewayManager:
    def __init__(self, token: str, intents: int, endpointclient: EndpointManager):
        self.token = token
        self.intents = intents
        self.ws_url = asyncio.run(endpointclient.send_request(method="get", route="/gateway")).data["url"]
        self.client = aiohttp.ClientSession()
        self.ws = self.client.ws_connect(self.ws_url)
        self.HB_INT: int | None = None
        self.current_payload: Payload | None = None
        self.guild_count: int | None = None
        self.captured_app_info: None | AppInfo = None
        self.session_id: None | str | int = None
        self.resume_url: None | str = None
        self.current_seq: int | None = None

    async def _abstractor(self) -> Payload:
        async with self.ws as ws:
            serialized = await ws.receive_json()
            payloaded = Payload(serialized["op"], serialized["d"], serialized["t"], serialized["s"])
            self.current_payload = payloaded
            return payloaded

    async def _handle_heartbeats(self):
        event = await self._abstractor()
        jsonized = None
        if event.code == OPCODES.EVENT:
            payload = Payload(code=OPCODES.HEARTBEAT, d=event.seq)
            jsonized = payload.jsonize()
            self.current_seq = event.seq
        else:
            payload = Payload(code=1, d=None)
            jsonized = payload.jsonize()
        async with self.ws as ws:
            if event.code == OPCODES.HELLO:
                await asyncio.sleep(float(self.HB_INT) * uniform(float(0), float(1)))
            else:
                await asyncio.sleep(float(self.HB_INT))
                await ws.send_str(data=jsonized)
                await self._abstractor()

    async def _hand_shake(self):
        async with self.ws as ws:
            hb_int = await self._abstractor()
            self.HB_INT = hb_int.data
            initiatelogging.info(f"Received HELLO event. Initiating heartbeat at {self.HB_INT / 1000.:2f} seconds.")
            firstpayload = Payload(code=OPCODES.IDENTIFY, d={
                "token": self.token,
                "properties": {
                    "os": "windows" if os.name == "nt" else "linux",
                    "browser": "discmoji",
                    "device": "discmoji"
                },
                "intents": self.intents
            })
            jsonized = firstpayload.jsonize()
            await ws.send_str(jsonized)
            capture_guild_count = await self._abstractor()
            if capture_guild_count.code is None:
                self.guild_count = len(capture_guild_count.data["guilds"])
                initiatelogging.info(f"Received READY event. Connected to gateway at session id: {capture_guild_count.data['session_id']}, as {capture_guild_count.data['application']['bot']['username']}#{capture_guild_count.data['application']['bot']['discriminator']}")
                self.captured_app_info = AppInfo(capture_guild_count.data["application"])
                self.session_id = capture_guild_count.data["session_id"]

    async def _reconnect_with_data(self):
        if self.current_payload.code == OPCODES.RECONNECT:
            initiatelogging.info("Gateway sent a RECONNECT event. Initiating reconnect process . . .")
            self.client = aiohttp.ClientSession()
            self.ws = self.client.ws_connect(self.resume_url)
            async with self.ws as ws:
                try:
                    sending = Payload(code=6, d={
                        "token": self.token,
                        "session_id": self.session_id,
                        "seq": self.current_seq
                    })
                    jsonized = sending.jsonize()
                    await ws.send_str(jsonized)
                    response = await ws.receive_json()
                    if response["op"] == OPCODES.RESUME:
                        initiatelogging.info("Successfully reconnected to gateway using new url.")
                except aiohttp.ClientError as e:
                    raise DiscmojiAPIError(f"Discmoji couldn't reconnect to the gateway. {e.args}. raw payload: {self.current_payload.data}")
