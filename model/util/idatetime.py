from abc import abstractmethod, ABCMeta
from datetime import datetime


class IDateTime(metaclass=ABCMeta):
    @abstractmethod
    def now(self) -> datetime:
        pass

    @abstractmethod
    def utcnow(self) -> datetime:
        pass
