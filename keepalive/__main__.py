import logging
import asyncio

from os import environ

from .keepalive import start

if environ.get("DEBUG"):
    logging.basicConfig(
        format="%(levelname)s - %(name)s - %(message)s", level=logging.DEBUG
    )
else:
    logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.INFO)

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
except KeyboardInterrupt:
    pass
