from typing import *
import functools
import asyncio
from asyncio import gather


class Command:
    """Represents a prefix command. Not for slash commands, those have a seperate class."""
    def __init__(self,/,name: str):
        self.name = name
        self.callback: Callable | None = None
        self.__error_handlers: List[Callable] = []
        
    async def __call__(self, *args, **kwargs) -> None:
        if not self.callback:
            raise ValueError("Callback function is not set for the command.")
        try:
            await self.callback(*args, **kwargs)
        except Exception as e:
            tasks = []
            for handler in self.__error_handlers:
                tasks.append(handler(e))
            await gather(*tasks)

    def error(self, function: Callable) -> Callable:
        self.__error_handlers.append(function)
        return function

    def __repr__(self):
        return f"<Command name={self.name}>"
