import logging
from logging.handlers import RotatingFileHandler
from typing import Callable

import inject

from util.iapp_folders import IAppFolders
from util.ilogger import ILogger


class Logger(ILogger):
    _log_format = "%(asctime)s %(levelname)s: %(message)s"

    def __init__(self):
        self._logger = logging.getLogger()

        folders = inject.instance(IAppFolders)

        logs_folder = f"{folders.get_logs_folder()}/bot.log"

        file_handler = RotatingFileHandler(logs_folder, maxBytes=1048576, backupCount=3)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(self._log_format))

        self._logger.addHandler(file_handler)

        self.set_level(logging.INFO)

    def info(self, message: str):
        return self._logger.info(message)

    def debug(self, message: str):
        self._logger.debug(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def critical(self, message: str):
        self._logger.critical(message)

    def exception(self, message: str):
        self._logger.exception(message)

    def set_level(self, level: int):
        self._logger.setLevel(level)

    def register_logging_handler(self, handler: Callable[[str], None], level: int = logging.INFO):
        handler = LoggingHandler(handler)
        handler.setFormatter(logging.Formatter(self._log_format))
        handler.setLevel(level)

        self._logger.addHandler(handler)


class LoggingHandler(logging.Handler):
    def __init__(self, handler: Callable[[str], None]):
        super().__init__()

        self._handler = handler

    def emit(self, record):
        self._handler(self.format(record))
