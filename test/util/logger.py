import os
import tempfile
from unittest import TestCase
from unittest.mock import Mock

import inject

from util.iapp_folders import IAppFolders
from util.logger import Logger


class TestLogger(TestCase):
    def setUp(self):
        self.folders_mock = Mock()

        inject.clear_and_configure(lambda binder: binder.bind(IAppFolders, self.folders_mock))

    def test_logging(self):
        tempdir = tempfile.mkdtemp()

        self.folders_mock.get_logs_folder.return_value = tempdir

        logger = Logger()

        logger.info("test_message")

        self.assertTrue(os.path.exists(os.path.join(tempdir, "bot.log")))

        with open(os.path.join(tempdir, "bot.log"), "r") as f:
            self.assertIn("INFO: test_message", f.read())

    def test_handler(self):
        tempdir = tempfile.mkdtemp()

        self.folders_mock.get_logs_folder.return_value = tempdir

        logger = Logger()

        handler_ran = []

        def handler(message):
            handler_ran.append(message)

            self.assertIn("INFO: test_message", message)

        logger.register_logging_handler(handler)

        logger.info("test_message")

        self.assertEqual(1, len(handler_ran))
        self.assertIn("INFO: test_message", handler_ran[0])
