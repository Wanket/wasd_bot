from dataclasses import dataclass
from typing import Dict, Tuple

from model.settings.answer_settings import AnswerSettings


@dataclass
class BotSettings:
    token: str
    commands: Dict[str, Dict[str, AnswerSettings]]
