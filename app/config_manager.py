import json


class ConfigManager:
    def __init__(self, config_file_name=None):
        if config_file_name:
            with open(config_file_name) as f:
                config = json.load(f)

            self.db_path = config['db_path']
            self.logger_path = config['logger_path']
        else:
            self.db_path = None
            self.logger_path = None
