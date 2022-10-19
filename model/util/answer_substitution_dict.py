import re
from typing import Match, List, Set, Any


class AnswerSubstitutionDict(dict):
    _random_number_regex = re.compile(r"random_number\((-?\d+),\s*(-?\d+)\)")

    # example @(any non space symbol) -> list of users
    _users_tagged_regex = re.compile(r"@\w+")

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
            users_list: List[str],
            args: str,
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
            "users_tagged": self._get_users_tagged(args, users_list),
        })

        self._random_number = random_number

    def __getitem__(self, key: str):
        match = AnswerSubstitutionDict._random_number_regex.fullmatch(key)
        if match:
            return self._get_random_number(match)

        return super().__getitem__(key)

    def _get_random_number(self, match: Match[str]) -> str:
        from_number = int(match.group(1))
        to_number = int(match.group(2))

        if from_number > to_number:
            return "(random_number: неверный диапазон)"

        return str(int(self._random_number * (to_number - from_number) + from_number))

    @staticmethod
    def _get_users_tagged(args: str, users_list: List[str]) -> str:
        users = {user.lower() for user in users_list}

        match = AnswerSubstitutionDict._users_tagged_regex.findall(args) or []

        return ", ".join((filter(lambda x: x[1:].lower() in users, match))) or "(не указан зритель)"
