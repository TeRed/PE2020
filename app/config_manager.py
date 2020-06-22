import json
import abc
import i18n


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
        self.language = ''
        self.db_path = ''
        self.logger_path = ''
        if config_file_name:
            try:
                with open(config_file_name) as f:
                    config = json.load(f)
                self.db_path = config['db_path']
                self.language = config['language']
                self.logger_path = config['logger_path']
            except IOError:
                print(f"WARNING: {i18n.t('CONFIG_FILE_NOT_FOUND')}")
        if not self.db_path.endswith(".json"):
            self.db_path = 'db.json'
        if not self.logger_path.endswith(".json"):
            self.logger_path = 'logger.json'
        if not self.language:
            self.language = 'en'

    def get_db_path(self):
        return self.db_path

    def get_logger_path(self):
        return self.logger_path

    def set_language(self, language):
        self.language = language
        i18n.set('locale', self.language)

    def save_configuration(self, config_file_name=None):
        config = {'db_path': self.db_path, 'language': self.language, 'logger_path': self.logger_path}

        if config_file_name:
            with open(config_file_name, 'w') as f:
                json.dump(config, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        else:
            with open('config.json', 'w') as f:
                json.dump(config, f, default=lambda o: o.__dict__, sort_keys=True, indent=4)
