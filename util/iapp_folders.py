from abc import ABCMeta, abstractmethod


class IAppFolders(metaclass=ABCMeta):
    @abstractmethod
    def get_settings_folder(self):
        pass

    @abstractmethod
    def get_logs_folder(self):
        pass
