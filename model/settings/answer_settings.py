from dataclasses import dataclass
from typing import Optional


@dataclass
class AnswerSettings:
    template: Optional[str]
    ban: bool
