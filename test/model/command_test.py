from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

import inject

from api.iwapi import IWapi
from model.answer import Answer
from model.command import Command
from model.user_message import UserMessage
from model.util.idatetime import IDateTime
from model.util.irandom import IRandom


class TestCommand(TestCase):
    def setUp(self):
        self.wapi_mock = Mock()
        self.random_mock = Mock()
        self.date_time_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IWapi, self.wapi_mock)
            .bind(IRandom, self.random_mock)
            .bind(IDateTime, self.date_time_mock)
        )

    def test_rate(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.date_time_mock.now.return_value = datetime(2020, 1, 1)

        self.date_time_mock.return_value = datetime(2020, 1, 1)

        first_answer = Answer("first_answer", False)
        second_answer = Answer("second_answer", False)

        command = Command([(2, first_answer), (1, second_answer)], 0)

        self.random_mock.randint.side_effect = [1, 2, 3]

        for i, expected in enumerate(["first_answer", "first_answer", "second_answer"]):
            command.exec(UserMessage(0, "", ""))
            self.wapi_mock.send_message.assert_called_with(expected)
            self.random_mock.randint.assert_called_with(1, 3)

    def test_timeout(self):
        self.wapi_mock.get_stream_time.return_value = 12345
        self.random_mock.randint.return_value = 1

        self.date_time_mock.now.side_effect = [datetime(2020, 1, 1), datetime(2020, 1, 1, 0, 0, 2), datetime(2020, 1, 1, 0, 0, 5)]

        command = Command([(1, Answer("test", False))], 4)

        command.exec(UserMessage(42, "", ""))
        self.wapi_mock.send_message.assert_called_with("test")

        command.exec(UserMessage(42, "", ""))
        self.wapi_mock.send_message.assert_called_once()

        command.exec(UserMessage(42, "", ""))
        self.wapi_mock.send_message.assert_called_with("test")
