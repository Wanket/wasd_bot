import inject
import jsonpickle
from unqlite import UnQLite

from model.settings.bot_settings import BotSettings
# noinspection PyUnresolvedReferences
from repository.irepository import IRepository
from util.iapp_folders import IAppFolders


class Repository(IRepository):
    _bot_settings_key = "bot_settings"

    def __init__(self):
        folders = inject.instance(IAppFolders)

        self._db = UnQLite(f"{folders.get_settings_folder()}/bot.db")

    def get_bot_settings(self) -> BotSettings:
        if self._bot_settings_key not in self._db:
            return BotSettings("", "", {})

        settings = jsonpickle.loads(self._db[self._bot_settings_key])

        self._check_migration(settings)

        return settings

    def set_bot_settings(self, bot_settings: BotSettings):
        self._db[self._bot_settings_key] = jsonpickle.dumps(bot_settings)

        self._db.commit()

    @staticmethod
    def _check_migration(bot_settings: BotSettings):
        for command in bot_settings.commands.values():
            for answer in command.answers.values():
                if not hasattr(answer, "sticker_name"):
                    answer.sticker_name = None
