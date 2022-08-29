class IWapi:
    def send_message(self, text: str):
        raise NotImplemented

    def ban_user(self, user_id: int):
        raise NotImplemented

    def get_stream_time(self) -> int:
        raise NotImplemented

    def get_game_name(self) -> str:
        raise NotImplemented

    def start_listen(self, token: str):
        raise NotImplemented
