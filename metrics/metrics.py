import os
from typing import Tuple, Dict

import inject

# noinspection PyUnresolvedReferences
from metrics.imetrics import IMetrics
from model.util.idatetime import IDateTime
from util.iapp_folders import IAppFolders
from util.ilogger import ILogger


class Metrics(IMetrics):
    def __init__(self):
        folders = inject.instance(IAppFolders)

        logger = inject.instance(ILogger)

        self._metrics_folder = f"{folders.get_settings_folder()}/metrics"

        os.makedirs(self._metrics_folder, exist_ok=True)

        logger.info(f"{self.__class__.__name__}: metrics folder: {self._metrics_folder}")

        self._metrics: Dict[str, Dict[Tuple[str, ...], float]] = {}

        self._time = inject.instance(IDateTime)

    def inc_metric(self, metric_name: str, *labels: str):
        self.add_metric(metric_name, 1, *labels)

    def add_metric(self, metric_name: str, value: float, *labels: str):
        if metric_name not in self._metrics:
            self._metrics[metric_name] = {}

        if labels not in self._metrics[metric_name]:
            self._metrics[metric_name][labels] = 0

        self._metrics[metric_name][labels] += value

        with open(f"{self._metrics_folder}/{metric_name}.csv", "a") as f:
            if len(labels) != 0:
                f.write(f"{','.join(labels)},{self._metrics[metric_name][labels]},{self._time.now().timestamp()}\n")
            else:
                f.write(f"{self._metrics[metric_name][labels]},{self._time.now().timestamp()}\n")
