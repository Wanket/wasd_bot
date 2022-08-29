from dataclasses import dataclass


@dataclass
class UserMessage:
    user_id: int
    user_name: str
    text: str
