from random import Random
from unittest import TestCase
from unittest.mock import Mock

import inject

from api.iwapi import IWapi
from model.bot import Bot
from model.settings.answer_settings import AnswerSettings
from model.settings.bot_settings import BotSettings
from model.user_message import UserMessage
from model.util.irandom import IRandom
from repository.irepository import IRepository
from util.ilogger import ILogger


class TestBot(TestCase):
    def setUp(self):
        self.wapi_mock = Mock()
        self.repository_mock = Mock()
        self.logger_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IWapi, self.wapi_mock)
            .bind(IRepository, self.repository_mock)
            .bind(ILogger, self.logger_mock)
            .bind(IRandom, Random())
        )

    def test_set_settings(self):
        self.repository_mock.get_bot_settings.return_value = BotSettings(token="", commands={})

        bot = Bot()

        settings = BotSettings(token="test_token", commands={
            "test_command": [(1, AnswerSettings("message_template", False))]
        })

        bot.set_settings(settings)

        self.repository_mock.set_bot_settings.assert_called_once_with(settings)

    def test_get_settings(self):
        settings = BotSettings(token="test_token", commands={
            "test_command": [(1, AnswerSettings("message_template", False))]
        })

        self.repository_mock.get_bot_settings.return_value = settings

        bot = Bot()

        settings = bot.get_settings()

        self.assertEqual(settings, settings)

    def test_on_message(self):
        settings = BotSettings(token="test_token", commands={
            "test_command": [(1, AnswerSettings("message_template", False))]
        })

        self.wapi_mock.get_stream_time.return_value = 12345

        self.repository_mock.get_bot_settings.return_value = settings

        bot = Bot()

        message = UserMessage(42, "user_name", "!test_command")

        bot.on_message(message)

        self.wapi_mock.send_message.assert_called_once_with("message_template")

    def test_repository_exceptions(self):
        self.repository_mock.get_bot_settings.side_effect = Exception("test_exception")

        bot = Bot()

        settings = bot.get_settings()

        self.assertEqual(settings, BotSettings("", {}))

        self.logger_mock.error.assert_called_with("Bot: error while loading bot settings, error text: test_exception, loading defaults")

        self.repository_mock.set_bot_settings.side_effect = Exception("test_exception")

        bot.set_settings(settings)

        self.logger_mock.error.assert_called_with("Bot: error while saving bot settings, error text: test_exception")
