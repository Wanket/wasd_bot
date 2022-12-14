from datetime import datetime
from random import Random
from unittest import TestCase
from unittest.mock import Mock, call

import inject

from api.iwapi import IWapi
from model.bot import Bot
from model.settings.answer_settings import AnswerSettings
from model.settings.bot_settings import BotSettings
from model.settings.command_settings import CommandSettings
from model.user_message import UserMessage
from model.util.idatetime import IDateTime
from model.util.irandom import IRandom
from repository.irepository import IRepository
from util.ilogger import ILogger


class TestBot(TestCase):
    def setUp(self):
        self.wapi_mock = Mock()
        self.repository_mock = Mock()
        self.logger_mock = Mock()
        self.date_time_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IWapi, self.wapi_mock)
            .bind(IRepository, self.repository_mock)
            .bind(ILogger, self.logger_mock)
            .bind(IRandom, Random())
            .bind(IDateTime, self.date_time_mock)
        )

    def test_set_settings(self):
        self.repository_mock.get_bot_settings.return_value = BotSettings(channel="", token="", commands={})

        bot = Bot()

        settings = BotSettings(token="test_token", commands={
            "test_command": CommandSettings(0, {"test_answer": AnswerSettings(1, "message_template", None, False)})
        }, channel="test_channel")

        bot.set_settings(settings)

        self.repository_mock.set_bot_settings.assert_called_once_with(settings)

    def test_get_settings(self):
        settings = BotSettings(token="test_token", commands={
            "test_command": CommandSettings(0, {"test_answer": AnswerSettings(1, "message_template", None, False)})
        }, channel="test_channel")

        self.repository_mock.get_bot_settings.return_value = settings

        bot = Bot()

        settings = bot.get_settings()

        self.assertEqual(settings, settings)

    def test_on_message(self):
        settings = BotSettings(token="test_token", commands={
            "Test_Command": CommandSettings(0, {"test_answer": AnswerSettings(1, "message_template", None, False)})
        }, channel="test_channel")

        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = []

        self.date_time_mock.now.return_value = datetime(2020, 1, 1)

        self.repository_mock.get_bot_settings.return_value = settings

        bot = Bot()

        message = UserMessage(42, "user_name", "!test_command")

        bot.on_message(message)

        message = UserMessage(42, "user_name", "!TeSt_cOmMaNd")

        bot.on_message(message)

        self.wapi_mock.send_message.assert_has_calls([call("message_template"), call("message_template")])

    def test_repository_exceptions(self):
        self.repository_mock.get_bot_settings.side_effect = Exception("test_exception")

        bot = Bot()

        settings = bot.get_settings()

        self.assertEqual(settings, BotSettings("", "", {}))

        self.logger_mock.error.assert_called_with("Bot: error while loading bot settings, error text: test_exception, loading defaults")

        self.repository_mock.set_bot_settings.side_effect = Exception("test_exception")

        bot.set_settings(settings)

        self.logger_mock.error.assert_called_with("Bot: error while saving bot settings, error text: test_exception")

    def test_many_words(self):
        settings = BotSettings(token="test_token", commands={
            "Test Command": CommandSettings(0, {"test_answer": AnswerSettings(1, "Test Command", None, False)}),
            "Test": CommandSettings(0, {"test_answer": AnswerSettings(1, "Test", None, False)}),
        }, channel="test_channel")

        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = []

        self.date_time_mock.now.return_value = datetime(2020, 1, 1)

        self.repository_mock.get_bot_settings.return_value = settings

        bot = Bot()

        message = UserMessage(0, "", "!test command")

        bot.on_message(message)

        message = UserMessage(0, "", "!test another")

        bot.on_message(message)

        self.wapi_mock.send_message.assert_has_calls([call("Test Command"), call("Test")])
