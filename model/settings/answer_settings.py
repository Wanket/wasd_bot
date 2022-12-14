from dataclasses import dataclass
from typing import Optional


@dataclass
class AnswerSettings:
    rate: int
    template: Optional[str]
    sticker_name: Optional[str]
    ban: bool
