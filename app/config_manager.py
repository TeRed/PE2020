import json
import abc


class DbConfigManagerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_db_path(self):
        raise NotImplementedError


class LoggerConfigManagerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_logger_path(self):
        raise NotImplementedError


class ConfigManager(DbConfigManagerInterface, LoggerConfigManagerInterface):
    def __init__(self, config_file_name=None):
        if config_file_name:
            with open(config_file_name) as f:
                config = json.load(f)

            self.db_path = config['db_path']
            self.logger_path = config['logger_path']
        else:
            self.db_path = None
            self.logger_path = None

    def get_db_path(self):
        return self.db_path

    def get_logger_path(self):
        return self.logger_path
