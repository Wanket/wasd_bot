from abc import abstractmethod, ABCMeta


class IWapi(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, text: str):
        pass

    @abstractmethod
    def ban_user(self, user_id: int):
        pass

    @abstractmethod
    def get_stream_time(self) -> int:
        pass

    @abstractmethod
    def get_game_name(self) -> str:
        pass

    @abstractmethod
    def start_listen(self, token: str):
        pass
