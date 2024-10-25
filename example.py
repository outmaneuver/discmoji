import discmoji
from discmoji import *
import asyncio

Client = Bot(token="blah blah",intents=123213123) 

# this is subject to change


@Client.command(name="test1")
async def commd(ctx: Invoked):
    try:
        await Client.get_guild(1234567)
    except Exception as e:
        print(f"Error in command: {e}")

@commd.error()
async def error_cool(ctx: Invoked, error: Exception):
    print("ooh thank you demo-py!!")

asyncio.run(Client.connect)
