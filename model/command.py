from datetime import datetime, timedelta
from typing import List, Tuple, Dict

import inject

from model.answer import Answer
from model.user_message import UserMessage
from model.util.idatetime import IDateTime
from model.util.irandom import IRandom


class Command:
    def __init__(self, answers: List[Tuple[int, Answer]], timeout: int):
        self._answers = answers
        self._sum_rates = sum(a[0] for a in answers)

        self._timeout = timeout
        self._exec_history: Dict[int, datetime] = {}

        self._random = inject.instance(IRandom)
        self._time = inject.instance(IDateTime)

    def exec(self, message: UserMessage):
        current_time = self._time.now()

        if message.user_id not in self._exec_history:
            self._exec_history[message.user_id] = current_time - timedelta(seconds=self._timeout)

        if (current_time - self._exec_history[message.user_id]).seconds < self._timeout:
            return

        self._exec_history[message.user_id] = current_time

        rate = self._random.randint(1, self._sum_rates)

        for answer in self._answers:
            if rate <= answer[0]:
                answer[1].exec(message)

                break

            rate -= answer[0]
