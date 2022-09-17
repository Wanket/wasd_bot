from typing import Optional

import inject
from lazy import lazy

from api.iwapi import IWapi
from model.user_message import UserMessage
from model.util.answer_substitution_dict import AnswerSubstitutionDict
from model.util.answer_substitution_template import AnswerSubstitutionTemplate
from model.util.irandom import IRandom


class Answer:
    def __init__(self, template: Optional[str], ban: bool):
        self._template = AnswerSubstitutionTemplate(template) if template else None
        self._ban = ban

        self._rand = inject.instance(IRandom)

    def exec(self, message: UserMessage):
        if self._ban:
            self._wapi.ban_user(message.user_id)

        if self._template:
            self._wapi.send_message(self._prepare_message(message))

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
