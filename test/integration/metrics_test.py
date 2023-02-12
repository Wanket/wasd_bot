import tempfile
import unittest
from datetime import datetime
from unittest.mock import Mock

import inject

from metrics.metrics import Metrics
from model.util.idatetime import IDateTime
from util.iapp_folders import IAppFolders
from util.ilogger import ILogger


class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.folders_mock = Mock()
        self.logger_mock = Mock()
        self.time_mock = Mock()

        inject.clear_and_configure(
            lambda binder: binder
            .bind(IAppFolders, self.folders_mock)
            .bind(ILogger, self.logger_mock)
            .bind(IDateTime, self.time_mock)
        )

    def test_metrics(self):
        tempdir = tempfile.mkdtemp()

        self.folders_mock.get_settings_folder.return_value = tempdir

        metrics = Metrics()

        self.logger_mock.info.assert_called_once_with(f"Metrics: metrics folder: {tempdir}/metrics")

        self.time_mock.now.return_value = datetime(2020, 1, 1)

        metrics.inc_metric("test_metric", "label1", "label2")

        self.time_mock.now.return_value = datetime(2020, 1, 2)

        metrics.add_metric("test_metric", 43, "label1", "label2")

        with open(f"{tempdir}/metrics/test_metric.csv") as f:
            self.assertEqual(f.readline(), f"label1,label2,1,{datetime(2020, 1, 1).timestamp()}\n")
            self.assertEqual(f.readline(), f"label1,label2,44,{datetime(2020, 1, 2).timestamp()}\n")

    def test_metrics_empty_label(self):
        tempdir = tempfile.mkdtemp()

        self.folders_mock.get_settings_folder.return_value = tempdir

        metrics = Metrics()

        self.time_mock.now.return_value = datetime(2020, 1, 1)

        metrics.inc_metric("test_metric")

        with open(f"{tempdir}/metrics/test_metric.csv") as f:
            self.assertEqual(f.readline(), f"1,{datetime(2020, 1, 1).timestamp()}\n")
