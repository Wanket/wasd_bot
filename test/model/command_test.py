from unittest import TestCase
from unittest.mock import Mock

import inject

from api.iwapi import IWapi
from model.answer import Answer
from model.command import Command
from model.user_message import UserMessage
from model.util.irandom import IRandom


class TestCommand(TestCase):
    def setUp(self):
        self.wapi_mock = Mock()
        self.random_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IWapi, self.wapi_mock)
            .bind(IRandom, self.random_mock)
        )

    def test_rate(self):
        self.wapi_mock.get_stream_time.return_value = 12345

        first_answer = Answer("first_answer", False)
        second_answer = Answer("second_answer", False)

        command = Command([(2, first_answer), (1, second_answer)])

        self.random_mock.randint.side_effect = [1, 2, 3]

        for i, expected in enumerate(["first_answer", "first_answer", "second_answer"]):
            command.exec(UserMessage(0, "", ""))
            self.wapi_mock.send_message.assert_called_with(expected)
            self.random_mock.randint.assert_called_with(1, 3)
