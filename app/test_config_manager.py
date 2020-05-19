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
        config = {'db_path': 'db.json', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)

        # When
        config_manager = ConfigManager(self.config_file_name)

        # Then
        self.assertEqual(config_manager.db_path, "db.json")
        self.assertEqual(config_manager.logger_path, "logger.json")

    def test__init__2(self):
        # When
        config_manager = ConfigManager()

        # Then
        self.assertIsNone(config_manager.db_path)
        self.assertIsNone(config_manager.logger_path)


if __name__ == '__main__':
    unittest.main()
