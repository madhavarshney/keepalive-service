import asyncio
import logging

from collections import defaultdict
from typing import Optional, Tuple

import aiohttp

from .discord_notifications import on_service_healthy, on_service_error
from .types import Config, Service, State
from .utils import load_config, get_html_title

logger = logging


async def get_service_health(
    service: Service, session: aiohttp.ClientSession
) -> Tuple[bool, Optional[str]]:
    """
    Get the health of a service based on its configuration.
    """
    check = service["check"]

    async with session.get(check["url"]) as response:
        text = await response.text()

        if check["type"] == "REPL_HTTP_SERVICE":
            healthy = text == check["data"]

            if not healthy:
                title = get_html_title(text)

                return (False, title or "Unknown")

            return (healthy, None)

        elif check["type"] == "HTML_TITLE":
            title = get_html_title(text)

            if not title:
                return (False, "HTML title regex did not match!")

            if title == check["data"]:
                return (True, None)
            else:
                return (False, title)

        else:
            # TODO: better error handling
            raise RuntimeError("Unsupported check type.")


async def check_service(
    config: Config, service: Service, state: State, session: aiohttp.ClientSession
) -> None:
    """
    Check a service and send notifications.
    """
    logger.debug(f"Checking service {service['name']}...")

    try:
        healthy, output = await get_service_health(service, session)
        prev_healthy = state[service["name"]]

        if not healthy:
            logger.info(f"Service {service['name']} is not healthy!")
            await on_service_error(config, service, session, output or "Unknown Error")

        elif healthy and not prev_healthy:
            logger.info(f"Service {service['name']} is healthy once again.")
            await on_service_healthy(config, service, session)

        state[service["name"]] = healthy

    except Exception as err:
        logger.exception(err)

    logger.debug(f"Service {service['name']} checked.")


async def watch(
    config: Config, service: Service, state: State, session: aiohttp.ClientSession
) -> None:
    """
    Monitor a particular service.
    """
    while True:
        await check_service(config, service, state, session)
        await asyncio.sleep(config["interval"])


async def start() -> None:
    """
    Start the keepalive service - loads the config and starts monitoring.
    """
    config = load_config()
    state: State = defaultdict(lambda: True)

    logger.info(
        f"Keepalive service started - monitoring {len(config['services'])} services"
    )

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *(watch(config, service, state, session) for service in config["services"])
        )
