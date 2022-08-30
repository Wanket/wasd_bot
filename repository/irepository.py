from abc import abstractmethod, ABCMeta

from model.settings.bot_settings import BotSettings


class IRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_bot_settings(self) -> BotSettings:
        pass

    @abstractmethod
    def set_bot_settings(self, bot_settings: BotSettings):
        pass
