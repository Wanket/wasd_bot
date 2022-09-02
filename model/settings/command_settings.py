from dataclasses import dataclass
from typing import Dict

from model.settings.answer_settings import AnswerSettings


@dataclass
class CommandSettings:
    timeout: int
    answers: Dict[str, AnswerSettings]
