import re

from typing import Optional

import yaml

from .types import Config


def load_config() -> Config:
    """
    Load app configuration.
    """
    with open("config.yaml") as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def get_html_title(content: str) -> Optional[str]:
    """
    Extract the title from an HTML string.

    NOTE: Yes, I know. Regex + HTML = no good.
    TODO: Replace.
    """
    match = re.search(
        r"<title>(.*)<\/title>", content, flags=re.MULTILINE | re.IGNORECASE
    )

    if match:
        return match.groups()[0]

    return None
