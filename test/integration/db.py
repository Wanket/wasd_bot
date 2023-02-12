import os
import tempfile
import unittest
from unittest.mock import Mock

import inject

from model.settings.answer_settings import AnswerSettings
from model.settings.bot_settings import BotSettings
from model.settings.command_settings import CommandSettings
from repository.repository import Repository
from util.iapp_folders import IAppFolders
from util.ilogger import ILogger


class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.folders_mock = Mock()
        self.logger_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IAppFolders, self.folders_mock)
            .bind(ILogger, self.logger_mock)
        )

    def test_save_load(self):
        tempdir = tempfile.mkdtemp()

        self.folders_mock.get_settings_folder.return_value = tempdir

        repo = Repository()

        self.logger_mock.info.assert_called_with(f"Repository: db folder: {tempdir}/bot.db")

        self.assertEqual(repo.get_bot_settings(), BotSettings("", "", {}))

        settings = BotSettings(token="test_token", commands={
            "test_command": CommandSettings(42, {"test_answer": AnswerSettings(1, "message_template", None, False)})
        }, channel="test_channel")

        repo.set_bot_settings(settings)

        self.assertEqual(repo.get_bot_settings(), settings)

        self.assertTrue(os.path.exists(os.path.join(tempdir, "bot.db")))
