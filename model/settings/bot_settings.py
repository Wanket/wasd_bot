from dataclasses import dataclass
from typing import Dict

from model.settings.command_settings import CommandSettings


@dataclass
class BotSettings:
    channel: str
    token: str
    commands: Dict[str, CommandSettings]
