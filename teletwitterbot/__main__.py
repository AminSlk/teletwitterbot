import asyncio
import logging

from teletwitterbot.bot import run, setup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    application = loop.run_until_complete(setup())
    run(application)
