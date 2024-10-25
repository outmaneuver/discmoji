class DiscmojiError(Exception):
    """ An error relating to the inner workings of Discmoji. """
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"Discmoji encountered an internal error: {self.msg}"

class DiscmojiAPIError(DiscmojiError):
    """ An error related to Discord API interactions in Discmoji. """
    def __init__(self, msg: str, status_code: int = None):
        super().__init__(msg)
        self.status_code = status_code

    def __str__(self):
        if self.status_code:
            return f"An error occurred when interacting with the Discord API: {self.msg} (Status Code: {self.status_code})"
        return f"An error occurred when interacting with the Discord API: {self.msg}"

class DiscmojiCommandError(DiscmojiError):
    """ An error related to bot commands using Discmoji. """
    def __init__(self, msg: str, command_name: str = None):
        super().__init__(msg)
        self.command_name = command_name

    def __str__(self):
        if self.command_name:
            return f"An error occurred when executing/creating the bot command '{self.command_name}': {self.msg}"
        return f"An error occurred when executing/creating a bot command: {self.msg}"

class DiscmojiRatelimit(Warning):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return f"Discmoji is currently being ratelimited. Rerun the bot in: {self.msg}s."

# For unknown/unspecified errors: `raise DiscmojiError("Error Message")`
# For Discord API errors: `raise DiscmojiAPIError("Error Message")`
# For command errors: `raise DiscmojiCommandError("Error Message")`
