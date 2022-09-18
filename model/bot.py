from copy import deepcopy
from typing import Dict

import inject
from lazy import lazy

from api.iwapi import IWapi
from model.answer import Answer
from model.command import Command
from model.user_message import UserMessage
from model.settings.bot_settings import BotSettings
from repository.irepository import IRepository
from util.ilogger import ILogger


class Bot:
    def __init__(self):
        self._repository = inject.instance(IRepository)
        self._logger = inject.instance(ILogger)

        self._settings = BotSettings("", "", {})
        self._commands: Dict[str, Command] = {}

        try:
            self._reload_settings(self._repository.get_bot_settings())
        except Exception as e:
            self._logger.error(f"{self.__class__.__name__}: error while loading bot settings, error text: {e}, loading defaults")

            self._reload_settings(BotSettings("", "", {}))

    def on_message(self, message: UserMessage):
        if not message.text.startswith("!"):
            return

        message.text = message.text[1:]

        lower_text = message.text.lower()

        max_length = 0
        max_command = None

        for command_name, command in self._commands.items():
            if lower_text.startswith(command_name) and len(command_name) > max_length:
                max_length = len(command_name)
                max_command = command

        if max_command:
            max_command.exec(message)

    def get_settings(self) -> BotSettings:
        return deepcopy(self._settings)

    def set_settings(self, bot_settings: BotSettings):
        try:
            self._repository.set_bot_settings(bot_settings)
        except Exception as e:
            self._logger.error(f"{self.__class__.__name__}: error while saving bot settings, error text: {e}")

            return

        self._reload_settings(bot_settings)

    def start_bot(self):
        self._logger.info(f"{self.__class__.__name__}: starting bot")

        self._wapi.start_listen(self._settings.token, self._settings.channel)

    def stop_bot(self):
        self._logger.info(f"{self.__class__.__name__}: stopping bot")

        self._wapi.stop_listen()

    def _reload_settings(self, bot_settings: BotSettings):
        self._settings = bot_settings

        commands = {}
        for name, command in bot_settings.commands.items():
            answers = []
            for _, answer_settings in command.answers.items():
                answers.append((answer_settings.rate, Answer(answer_settings.template, answer_settings.sticker_name, answer_settings.ban)))

            commands[name.lower()] = Command(answers, command.timeout)

        self._commands = commands

        self._logger.info(f"{self.__class__.__name__}: bot settings loaded/updated")

    @lazy
    def _wapi(self) -> IWapi:
        return inject.instance(IWapi)
