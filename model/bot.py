from typing import Dict

import inject

from model.answer import Answer
from model.command import Command
from model.user_message import UserMessage
from model.settings.bot_settings import BotSettings
from repository.irepository import IRepository


class Bot:
    def __init__(self):
        self._repository = inject.instance(IRepository)

        self._token: str = ""
        self._commands: Dict[str, Command] = {}

        self._reload_settings(self._repository.get_bot_settings())

    def on_message(self, message: UserMessage):
        if message.text.startswith("!"):
            words = message.text[1:].split()

            command = self._commands.get(words[0])
            if command:
                message.text = message.text[len(words[0]) + 1:]

                command.exec(message)

    def get_settings(self) -> BotSettings:
        return self._repository.get_bot_settings()

    def set_settings(self, bot_settings: BotSettings):
        self._repository.set_bot_settings(bot_settings)

        self._reload_settings(bot_settings)

    def _reload_settings(self, bot_settings: BotSettings):
        self._token = bot_settings.token

        commands = {}
        for name, command in bot_settings.commands.items():
            commands[name] = Command([(rate, Answer(answer_settings.template, answer_settings.ban)) for rate, answer_settings in command])

        self._commands = commands
