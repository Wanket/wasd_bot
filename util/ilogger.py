from abc import abstractmethod, ABCMeta
from typing import Callable


class ILogger(metaclass=ABCMeta):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def debug(self, message: str):
        pass

    @abstractmethod
    def warning(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def critical(self, message: str):
        pass

    @abstractmethod
    def exception(self, message: str):
        pass

    @abstractmethod
    def set_level(self, level: int):
        pass

    @abstractmethod
    def register_logging_handler(self, handler: Callable[[str], None]):
        pass
