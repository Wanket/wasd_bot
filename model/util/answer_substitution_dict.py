import re
from typing import Match


class AnswerSubstitutionDict(dict):
    def __init__(
            self,
            uptime: str,
            game_name: str,
            user_name: str,
            users_count_total: str,
            users_count_auth: str,
            users_count_anon: str,
            random_user: str,
            random_number: float,
    ):
        super().__init__()

        self.update({
            "uptime": uptime,
            "game_name": game_name,
            "user_name": user_name,
            "users_count_total": users_count_total,
            "users_count_auth": users_count_auth,
            "users_count_anon": users_count_anon,
            "random_user": random_user,
        })

        self._random_number = random_number

        self._random_number_regex = re.compile(r"random_number\((-?\d+),\s*(-?\d+)\)")

    def __getitem__(self, key: str):
        match = self._random_number_regex.fullmatch(key)
        if match:
            return self._get_random_number(match)

        return super().__getitem__(key)

    def _get_random_number(self, match: Match[str]) -> str:
        from_number = int(match.group(1))
        to_number = int(match.group(2))

        if from_number > to_number:
            return "(random_number: неверный диапазон)"

        return str(int(self._random_number * (to_number - from_number) + from_number))
