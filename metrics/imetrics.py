from abc import ABCMeta, abstractmethod


class IMetrics(metaclass=ABCMeta):
    @abstractmethod
    def inc_metric(self, metric_name: str, *labels: str):
        pass

    @abstractmethod
    def add_metric(self, metric_name: str, value: float, *labels: str):
        pass
