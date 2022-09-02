from string import Template
from typing import Optional

import inject
from lazy import lazy

from api.iwapi import IWapi
from model.user_message import UserMessage
from model.util.key_default_dict import KeyDefaultDict


class Answer:
    def __init__(self, template: Optional[str], ban: bool):
        self._template = Template(template) if template else None
        self._ban = ban

    def exec(self, message: UserMessage):
        if self._ban:
            self._wapi.ban_user(message.user_id)

        if self._template:
            self._wapi.send_message(self._prepare_message(message))

    def _prepare_message(self, message: UserMessage) -> str:
        users_total = self._wapi.get_users_count_total()
        users_auth = self._wapi.get_users_count_auth()
        users_anon = self._wapi.get_users_count_anon()

        return self._template.substitute(KeyDefaultDict(
            lambda x: f"${x}",
            uptime=Answer._format_time(self._wapi.get_stream_time()),
            game_name=self._wapi.get_game_name(),
            user_name=message.user_name,
            users_count_total=users_total if users_total is not None else "(нет данных)",
            users_count_auth=users_auth if users_auth is not None else "(нет данных)",
            users_count_anon=users_anon if users_anon is not None else "(нет данных)",
        ))

    @lazy
    def _wapi(self) -> IWapi:
        return inject.instance(IWapi)

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
