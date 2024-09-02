from typing import *
from .http import EndpointManager
from .gateway import GatewayManager
import asyncio
from .bot import Bot
from .member import GuildMember
from .guild import Guild




class Invoked:
    """A class that hosts the data of where a prefix command was used."""
    # A class that hosts the data of where a command was used
    def __init__(self,endpoint: EndpointManager,gateway: GatewayManager,bot: Bot):
        self._endpoint = endpoint
        self._gateway = gateway
        self._bot = bot
        # rest will be constructed by internal funcs
        self.member = ...
        self.message = ...
        self.messagerefs = ...
        self.channel = ...
        self.guild = ...
    
    
    def _construct(self):
        # constructs itself so it can be used while running a command
        self.member: GuildMember = GuildMember(self._gateway.current_payload.data["member"])
        self.guild: Guild = Guild(asyncio.run(self._endpoint.send_request(method="get",route=f"/guilds/{self._gateway.current_payload.data["guild_id"]}")).data)
            