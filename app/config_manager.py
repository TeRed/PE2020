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
        self.db_path = ''
        self.logger_path = ''
        if config_file_name:
            try:
                with open(config_file_name) as f:
                    config = json.load(f)
                self.db_path = config['db_path']
                self.logger_path = config['logger_path']
            except IOError:
                print("WARNING: Config file not found")
        if not self.db_path.endswith(".json"):
            self.db_path = 'db.json'
        if not self.logger_path.endswith(".json"):
            self.logger_path = 'logger.json'

    def get_db_path(self):
        return self.db_path

    def get_logger_path(self):
        return self.logger_path

    def save_configuration(self, config_file_name=None):
        config = {'db_path': self.db_path, 'logger_path': self.logger_path}

        if config_file_name:
            with open(config_file_name, 'w') as f:
                json.dump(config, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        else:
            with open('config.json', 'w') as f:
                json.dump(config, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)
