import unittest
import json
from os import remove
from config_manager import ConfigManager


class MyTestCase(unittest.TestCase):
    config_file_name = "test_config.json"

    def setUp(self):
        open(self.config_file_name, "w").close()

    def tearDown(self):
        remove(self.config_file_name)

    def test__init__(self):
        # Given
        config = {'db_path': 'db.json', 'language': 'en', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)

        # When
        config_manager = ConfigManager(self.config_file_name)

        # Then
        self.assertEqual(config_manager.db_path, "db.json")
        self.assertEqual(config_manager.language, "en")
        self.assertEqual(config_manager.logger_path, "logger.json")

    def test_default_config_parameters(self):
        # Given
        config_manager = ConfigManager()

        # Then
        self.assertEqual(config_manager.db_path, 'db.json')
        self.assertEqual(config_manager.language, 'en')
        self.assertEqual(config_manager.logger_path, 'logger.json')

    def test_save_config_to_file(self):
        # Given
        config = {'db_path': 'db.json', 'language': 'en', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)
        config_manager = ConfigManager(self.config_file_name)
        setattr(config_manager, 'db_path', 'db2.json')

        # When
        config_manager.save_configuration()

        # Then
        with open(self.config_file_name) as f:
            config = json.load(f)

        self.assertEqual(config['db_path'], 'db2.json')


if __name__ == '__main__':
    unittest.main()
