import textwrap

import aiohttp

from .types import Config, Service


async def send_discord_message(
    config: Config, session: aiohttp.ClientSession, content: str
) -> None:
    """
    Send a discord message through the configured webhook URL.
    """
    await session.post(
        config["discord_webhook_url"],
        json={
            "content": content,
        },
        raise_for_status=True,
    )


async def on_service_healthy(
    config: Config, service: Service, session: aiohttp.ClientSession
) -> None:
    """
    Notify discord webhook when a service is healthy.
    """
    await send_discord_message(
        config,
        session,
        textwrap.dedent(
            f"""
            :salad: **__{service['name']}__** :salad:

            Service looks healthy!

            {service['check']['url']}
            """
        ),
    )


async def on_service_error(
    config: Config, service: Service, session: aiohttp.ClientSession, output: str
) -> None:
    """
    Notify discord webhook when there is an error in a service.
    """
    await send_discord_message(
        config,
        session,
        textwrap.dedent(
            f"""
            :no_entry_sign: **__{service['name']}__** :no_entry_sign:

            Something is wrong: ```
            {output}
            ```
            {service['check']['url']}
            """
        ),
    )
