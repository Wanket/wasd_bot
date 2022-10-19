from typing import Optional, Tuple

import inject
from lazy import lazy

from api.iwapi import IWapi
from model.user_message import UserMessage
from model.util.answer_substitution_dict import AnswerSubstitutionDict
from model.util.answer_substitution_template import AnswerSubstitutionTemplate
from model.util.irandom import IRandom


class Answer:
    def __init__(self, template: Optional[str], sticker_name: Optional[str], ban: bool):
        self._template = AnswerSubstitutionTemplate(template) if template else None
        self._ban = ban
        self._sticker_name = sticker_name

        self._rand = inject.instance(IRandom)

    def exec(self, message: UserMessage):
        if self._ban:
            self._wapi.ban_user(message.user_id)

        if self._template:
            self._wapi.send_message(self._prepare_message(message))

        if self._sticker_name and self._sticker_name != "":
            self._wapi.send_sticker(self._sticker_name)

    def _prepare_message(self, message: UserMessage) -> str:
        users_total = self._wapi.get_users_count_total()
        users_auth = self._wapi.get_users_count_auth()
        users_anon = self._wapi.get_users_count_anon()

        users_list = self._wapi.get_users_list()

        return self._template.safe_substitute(AnswerSubstitutionDict(
            uptime=Answer._format_time(self._wapi.get_stream_time()),
            game_name=self._wapi.get_game_name(),
            user_name=message.user_name,
            users_count_total=users_total if users_total is not None else "(нет данных)",
            users_count_auth=users_auth if users_auth is not None else "(нет данных)",
            users_count_anon=users_anon if users_anon is not None else "(нет данных)",
            random_user=self._rand.choice(users_list) if users_list else "(чат пуст)",
            random_number=self._rand.random(),
            users_list=users_list,
            args=message.text,
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
            return f"{h} {Answer._format_hour(h)} {m} {Answer._format_minute(m)} {s} {Answer._format_second(s)}"
        elif m > 0:
            return f"{m} {Answer._format_minute(m)} {s} {Answer._format_second(s)}"
        else:
            return f"{s} {Answer._format_second(s)}"

    @staticmethod
    def _format_hour(h: int) -> str:
        return Answer._format_number(h, ("час", "часа", "часов"))

    @staticmethod
    def _format_minute(m: int) -> str:
        return Answer._format_number(m, ("минута", "минуты", "минут"))

    @staticmethod
    def _format_second(s: int) -> str:
        return Answer._format_number(s, ("секунда", "секунды", "секунд"))

    @staticmethod
    def _format_number(n: int, variants: Tuple[str, str, str]) -> str:
        if n % 10 == 1 and n != 11:
            return variants[0]

        if (n % 10 == 2 or n % 10 == 3 or n % 10 == 4) and n != 12 and n != 13 and n != 14:
            return variants[1]

        return variants[2]
