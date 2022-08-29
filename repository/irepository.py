from model.settings.bot_settings import BotSettings


class IRepository:
    def get_bot_settings(self) -> BotSettings:
        raise NotImplemented

    def set_bot_settings(self, bot_settings: BotSettings):
        raise NotImplemented
