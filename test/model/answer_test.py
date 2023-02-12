from unittest import TestCase
from unittest.mock import Mock, call

import inject

from api.iwapi import IWapi
from model.answer import Answer
from model.user_message import UserMessage
from model.util.irandom import IRandom


class TestAnswer(TestCase):
    def setUp(self):
        self.wapi_mock = Mock()
        self.random_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IWapi, self.wapi_mock)
            .bind(IRandom, self.random_mock)
        )

    def test_placeholder(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_game_name.return_value = "test game"
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        answer = Answer("время ${uptime}, игра ${game_name}, написал пользователь ${user_name}", None, False)
        answer.exec(UserMessage(42, "test_user", "test_message"))

        self.wapi_mock.get_stream_time.assert_called_once_with()
        self.wapi_mock.send_message.assert_called_once_with("время 3 часа 25 минут 45 секунд, игра test game, написал пользователь test_user")

    def test_smart_placeholder(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        answer = Answer("${user_name}name}", None, False)
        answer.exec(UserMessage(42, "${user_", ""))

        self.wapi_mock.send_message.assert_called_once_with("${user_name}")

    def test_ban(self):
        self.wapi_mock.get_stream_time.return_value = 12345

        answer = Answer("", None, True)
        answer.exec(UserMessage(42, "", ""))

        self.wapi_mock.ban_user.assert_called_once_with(42)

    def test_no_message_no_ban(self):
        self.wapi_mock.get_stream_time.return_value = 12345

        answer = Answer(None, None, False)
        answer.exec(UserMessage(42, "", ""))

        self.wapi_mock.send_message.assert_not_called()
        self.wapi_mock.ban_user.assert_not_called()

    def test_time(self):
        self.wapi_mock.get_stream_time.side_effect = [12345, 123, 12]
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        answer = Answer("время ${uptime}", None, False)

        for expected in ["время 3 часа 25 минут 45 секунд", "время 2 минуты 3 секунды", "время 12 секунд"]:
            answer.exec(UserMessage(42, "", ""))
            self.wapi_mock.send_message.assert_called_with(expected)

    def test_random_user(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = ["user1", "user2", "user3"]

        self.random_mock.choice.return_value = "user2"

        answer = Answer("рандомный пользователь ${random_user}", None, False)
        answer.exec(UserMessage(42, "", ""))

        self.wapi_mock.get_users_list.assert_called_once_with()
        self.random_mock.choice.assert_called_once_with(["user1", "user2", "user3"])
        self.wapi_mock.send_message.assert_called_once_with("рандомный пользователь user2")

    def test_random_user_empty(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = []

        answer = Answer("рандомный пользователь ${random_user}", None, False)
        answer.exec(UserMessage(42, "", ""))

        self.wapi_mock.get_users_list.assert_called_once_with()
        self.random_mock.choice.assert_not_called()
        self.wapi_mock.send_message.assert_called_once_with("рандомный пользователь (чат пуст)")

    def test_random_number(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        self.random_mock.random.return_value = 0.45

        answer = Answer("рандомное число ${random_number(1, 100)}", None, False)
        answer.exec(UserMessage(0, "", ""))

        self.random_mock.random.assert_called_once_with()
        self.wapi_mock.send_message.assert_called_once_with("рандомное число 45")

    def test_random_number_wrong_from_to(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        self.random_mock.random.return_value = 0.45

        answer = Answer("рандомное число ${random_number(100,1)}", None, False)
        answer.exec(UserMessage(0, "", ""))

        answer = Answer("рандомное число ${random_number(100, 100)}", None, False)
        answer.exec(UserMessage(0, "", ""))

        self.wapi_mock.send_message.assert_has_calls([
            call("рандомное число (random_number: неверный диапазон)"),
            call("рандомное число 100")
        ])

    def test_random_number_float(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        self.random_mock.random.return_value = 0.45

        answer = Answer("рандомное число ${random_number(1.100, 2)", None, False)
        answer.exec(UserMessage(0, "", ""))

        self.random_mock.random.assert_called_once_with()
        self.wapi_mock.send_message.assert_called_once_with("рандомное число ${random_number(1.100, 2)")

    def test_random_number_negative(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = ["test_user"]

        self.random_mock.random.return_value = 0.45

        answer = Answer("рандомное число ${random_number(-100, -100)}", None, False)
        answer.exec(UserMessage(0, "", ""))

        self.random_mock.random.assert_called_once_with()
        self.wapi_mock.send_message.assert_called_once_with("рандомное число -100")

    def test_functions(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = []

        answer = Answer("рандомный пользователь ${random_user()}", None, False)
        answer.exec(UserMessage(42, "", ""))

        self.wapi_mock.get_users_list.assert_called_once_with()
        self.wapi_mock.send_message.assert_called_once_with("рандомный пользователь ${random_user()}")

    def test_stickers(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.wapi_mock.get_users_list.return_value = []

        answer = Answer("", "Test_Sticker", False)
        answer.exec(UserMessage(0, "", ""))

        self.wapi_mock.send_message.assert_not_called()

        self.wapi_mock.send_sticker.assert_called_once_with("Test_Sticker")
