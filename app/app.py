import sys
from random import Random

import inject
from PySide6.QtWidgets import QApplication

from api.iwapi import IWapi
from api.wapi import Wapi
from metrics.imetrics import IMetrics
from metrics.metrics import Metrics
from model.util.datetime_impl import DateTime
from model.util.idatetime import IDateTime
from model.util.irandom import IRandom
from repository.irepository import IRepository
from repository.repository import Repository
from util.app_folders import AppFolders
from util.iapp_folders import IAppFolders
from util.ilogger import ILogger
from util.logger import Logger
from window.main_window.main_window import MainWindow


class App:
    def __init__(self):
        App._setup_di()

        self._logger = inject.instance(ILogger)

        self._setup_ui()

        self._logger.info(f"{self.__class__.__name__}: created")

    def __del__(self):
        inject.instance(IWapi).on_close()

        self._logger.info(f"{self.__class__.__name__}: destroyed")

    def run(self) -> int:
        self._logger.info(f"{self.__class__.__name__}: running")

        return self._q_app.exec_()

    def _setup_ui(self):
        self._q_app = QApplication(sys.argv)

        self._main_window = MainWindow()
        self._main_window.show()

    @staticmethod
    def _setup_di():
        inject.configure(
            lambda binder: binder
            .bind_to_constructor(IWapi, Wapi)
            .bind_to_constructor(IRandom, Random)
            .bind_to_constructor(IAppFolders, AppFolders)
            .bind_to_constructor(IRepository, Repository)
            .bind_to_constructor(ILogger, Logger)
            .bind_to_constructor(IDateTime, DateTime)
            .bind_to_constructor(IMetrics, Metrics)
        )
