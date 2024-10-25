import logging
from .logger import get_logger

logger = get_logger(__name__)

class DiscmojiError(Exception):
    """ An error relating to the inner workings of Discmoji. """
    def __init__(self, msg: str):
        self.msg = msg
        logger.error(f"DiscmojiError: {self.msg}")
    def __str__(self):
        return f"Discmoji encountered an internal error: {self.msg}"

class DiscmojiAPIError(DiscmojiError):
    """ An error related to Discord API interactions in Discmoji. """
    def __str__(self):
        return f"An error occurred when interacting with the Discord API: {self.msg}"

class DiscmojiCommandError(DiscmojiError):
    """ An error related to bot commands using Discmoji. """
    def __str__(self):
        return f"An error occurred when executing/creating a bot command: {self.msg}"

class DiscmojiRatelimit(Warning):
    def __init__(self, msg: str):
        self.msg = msg
        logger.warning(f"DiscmojiRatelimit: {self.msg}")
    def __str__(self):
        return f"Discmoji is currently being ratelimited. Rerun the bot in: {self.msg}s."

def handle_global_error(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

import sys
sys.excepthook = handle_global_error
