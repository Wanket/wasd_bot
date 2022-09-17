from abc import abstractmethod, ABCMeta
from typing import List, TypeVar


class IRandom(metaclass=ABCMeta):
    T = TypeVar("T")

    @abstractmethod
    def randint(self, a: int, b: int) -> int:
        pass

    @abstractmethod
    def random(self) -> float:
        pass

    @abstractmethod
    def choice(self, seq: List[T]) -> T:
        pass
