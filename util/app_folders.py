import os

import inject
from appdirs import user_log_dir, user_config_dir

from util.app_info import app_name
from util.iapp_folders import IAppFolders
from util.ilogger import ILogger


class AppFolders(IAppFolders):
    def __init__(self):
        self._app_name = app_name()

        os.makedirs(user_config_dir(self._app_name), exist_ok=True)
        os.makedirs(user_log_dir(self._app_name), exist_ok=True)

    def get_settings_folder(self) -> str:
        return user_config_dir(self._app_name)

    def get_logs_folder(self) -> str:
        return user_log_dir(self._app_name)
