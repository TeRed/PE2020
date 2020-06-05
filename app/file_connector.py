import json
import abc
from abc import ABCMeta


class FileConnector(metaclass=ABCMeta):
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def read_json_file(self):
        with open(self.get_file_path()) as f:
            load = json.load(f)
        return load

    def save_json_file(self, objs):
        with open(self.get_file_path(), 'w') as f:
            json.dump(objs, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @abc.abstractmethod
    def get_file_path(self):
        raise NotImplementedError


class LoggerFileConnector(FileConnector):
    def __init__(self, config_manager):
        super().__init__(config_manager)

    def get_file_path(self):
        return self.config_manager.get_logger_path()


class DbFileConnector(FileConnector):
    def __init__(self, config_manager):
        super().__init__(config_manager)

    def get_file_path(self):
        return self.config_manager.get_db_path()
