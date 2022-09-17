from abc import abstractmethod, ABCMeta
from typing import Optional, List


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
    def start_listen(self, token: str, channel_name: str):
        pass

    @abstractmethod
    def stop_listen(self):
        pass

    @abstractmethod
    def get_users_count_total(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_users_count_auth(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_users_count_anon(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_users_list(self) -> List[str]:
        pass
