from string import Template
from typing import Optional

import inject

from api.iwapi import IWapi
from model.user_message import UserMessage
from model.util.key_default_dict import KeyDefaultDict


class Answer:
    def __init__(self, template: Optional[str], ban: bool):
        self._wapi = inject.instance(IWapi)
        self._template = Template(template) if template else None
        self._ban = ban

    def exec(self, message: UserMessage):
        if self._template:
            self._wapi.send_message(self._prepare_message(message))

        if self._ban:
            self._wapi.ban_user(message.user_id)

    def _prepare_message(self, message: UserMessage) -> str:
        return self._template.substitute(KeyDefaultDict(
            lambda x: f"${x}",
            uptime=Answer._format_time(self._wapi.get_stream_time()),
            game_name=self._wapi.get_game_name(),
            user_name=message.user_name,
        ))

    @staticmethod
    def _format_time(t: int) -> str:
        h = t // 3600
        m = (t - h * 3600) // 60
        s = t - h * 3600 - m * 60

        if h > 0:
            return f"{h} часов {m} минут {s} секунд"
        elif m > 0:
            return f"{m} минут {s} секунд"
        else:
            return f"{s} секунд"
