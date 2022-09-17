import asyncio
from typing import Optional

import inject
from PySide6.QtCore import QThread, Signal, QObject

from util.ilogger import ILogger


class LogsThread(QThread):
    on_log = Signal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)

        self._logger = inject.instance(ILogger)

        self._event_loop = asyncio.new_event_loop()

    def run(self):
        self._logger.register_logging_handler(self._on_logs)

        asyncio.set_event_loop(self._event_loop)

        self._logger.info(f"{self.__class__.__name__}: running")

        self._event_loop.run_forever()

    def stop(self):
        self._logger.info(f"{self.__class__.__name__}: stopping")

        self._event_loop.call_soon_threadsafe(self._event_loop.stop)

        self.wait()

        self._event_loop.close()

        self._logger.info(f"{self.__class__.__name__}: stopped")

    def _on_logs(self, message):
        if not self._event_loop.is_closed():
            self._event_loop.call_soon_threadsafe(self._on_logs_impl, message)

    def _on_logs_impl(self, message):
        self.on_log.emit(message)
