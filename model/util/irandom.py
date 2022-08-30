from abc import abstractmethod, ABCMeta


class IRandom(metaclass=ABCMeta):
    @abstractmethod
    def randint(self, a, b) -> int:
        pass
