from __future__ import annotations

import os
from dotenv import load_dotenv

_SECRETS: dict = {}


def load_secrets() -> None:
    global _SECRETS

    load_dotenv()

    _SECRETS['TOKEN'] = str(os.getenv('DISCORD_TOKEN'))
    _SECRETS['GUILD'] = str(os.getenv('INFORMATYKA_GUILD_ID'))


def get_secret(secret: str) -> str | None:
    if secret in _SECRETS:
        return _SECRETS[secret]
    else:
        return None
