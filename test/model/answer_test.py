from unittest import TestCase
from unittest.mock import Mock

import inject

from api.iwapi import IWapi
from model.answer import Answer
from model.user_message import UserMessage


class TestAnswer(TestCase):
    def setUp(self):
        self.wapi_mock = Mock()

        inject.clear_and_configure(lambda binder: binder.bind(IWapi, self.wapi_mock))

    def test_placeholder(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_game_name.return_value = "test game"

        answer = Answer("время $uptime, игра $game_name, написал пользователь $user_name", False)
        answer.exec(UserMessage(42, "test_user", "test_message"))

        self.wapi_mock.get_stream_time.assert_called_once_with()
        self.wapi_mock.send_message.assert_called_once_with("время 3 часов 25 минут 45 секунд, игра test game, написал пользователь test_user")

    def test_smart_placeholder(self):
        self.wapi_mock.get_stream_time.return_value = 12345

        answer = Answer("$user_namename", False)
        answer.exec(UserMessage(42, "$user_", ""))

        self.wapi_mock.send_message.assert_called_once_with("$user_namename")

    def test_ban(self):
        self.wapi_mock.get_stream_time.return_value = 12345

        answer = Answer("$user_namename", True)
        answer.exec(UserMessage(42, "$user_", ""))

        self.wapi_mock.ban_user.assert_called_once_with(42)

    def test_no_message_no_ban(self):
        self.wapi_mock.get_stream_time.return_value = 12345

        answer = Answer(None, False)
        answer.exec(UserMessage(42, "", ""))

        self.wapi_mock.send_message.assert_not_called()
        self.wapi_mock.ban_user.assert_not_called()

    def test_time(self):
        self.wapi_mock.get_stream_time.side_effect = [12345, 123, 12]

        answer = Answer("время $uptime", False)

        for expected in ["время 3 часов 25 минут 45 секунд", "время 2 минут 3 секунд", "время 12 секунд"]:
            answer.exec(UserMessage(42, "", ""))
            self.wapi_mock.send_message.assert_called_with(expected)
