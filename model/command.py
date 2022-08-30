from typing import List, Tuple

import inject

from model.answer import Answer
from model.user_message import UserMessage
from model.util.irandom import IRandom


class Command:
    def __init__(self, answers: List[Tuple[int, Answer]]):
        self._answers = answers
        self._sum_rates = sum(a[0] for a in answers)
        self._random = inject.instance(IRandom)

    def exec(self, message: UserMessage):
        rate = self._random.randint(1, self._sum_rates)

        for answer in self._answers:
            if rate <= answer[0]:
                answer[1].exec(message)

                break

            rate -= answer[0]
