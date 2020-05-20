import unittest

from file_connector import LoggerFileConnector
from logger_connector import LoggerConnector
from article_logs import ArticleLogs
from log import Log
from config_manager import ConfigManager
from os import remove
import json


class MyTestCase(unittest.TestCase):

    config_file_name = 'test_logger.json'

    def setUp(self):
        open(self.config_file_name, "w").close()

    def tearDown(self):
        remove(self.config_file_name)

    def test_get_all_logs(self):
        # Given
        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Added"}]},
            {'id': '2', 'logs': [{"data": "08-05-2020", "text": "Added"}, {"data": "07-05-2020", "text": "Deleted"}]}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(logs, f)

        config_manager = ConfigManager()
        config_manager.logger_path = self.config_file_name
        logger = LoggerConnector(LoggerFileConnector(config_manager))

        expected = [
            ArticleLogs('1', [Log("08-05-2020", "Added")]),
            ArticleLogs('2', [Log("08-05-2020", "Added"), Log("07-05-2020", "Deleted")])
        ]

        # When
        logs = logger.get_all_logs()

        # Then
        self.assertListEqual(expected, logs)

    def test_get_logs_by_id(self):
        # Given
        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Added"}]},
            {'id': '2', 'logs': [{"data": "08-05-2020", "text": "Added"}, {"data": "07-05-2020", "text": "Deleted"}]}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(logs, f)

        config_manager = ConfigManager()
        config_manager.logger_path = self.config_file_name
        logger = LoggerConnector(LoggerFileConnector(config_manager))

        article_id = '1'
        expected = ArticleLogs('1', [Log("08-05-2020", "Added")])

        # When
        logs = logger.get_logs_by_id(article_id)

        # Then
        self.assertEqual(expected, logs)

    def test_get_borrowed_history(self):
        # Given
        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Added"}]},
            {
                'id': '2',
                'logs': [
                    {"data": "07-05-2020", "text": "Added"},
                    {"data": "08-05-2020", "text": "Borrowed"},
                    {"data": "10-05-2020", "text": "Returned"},
                    {"data": "11-05-2020", "text": "Borrowed"}
                ]
            }
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(logs, f)

        config_manager = ConfigManager()
        config_manager.logger_path = self.config_file_name
        logger = LoggerConnector(LoggerFileConnector(config_manager))

        expected = [
            Log('08-05-2020', 'Borrowed'),
            Log('10-05-2020', 'Returned'),
            Log('11-05-2020', 'Borrowed')
        ]

        # When
        logs = logger.get_borrow_history('2')

        # Then
        self.assertListEqual(expected, logs)

    def test_add_log(self):
        # Given
        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Added"}]}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(logs, f)

        config_manager = ConfigManager()
        config_manager.logger_path = self.config_file_name
        logger = LoggerConnector(LoggerFileConnector(config_manager))

        expected = [ArticleLogs('1', [Log("08-05-2020", "Added"), Log("20-05-2020", "Deleted")])]

        # When
        logger.add_log('1', Log("20-05-2020", "Deleted"))

        # Then
        self.assertListEqual(expected, logger.get_all_logs())


if __name__ == '__main__':
    unittest.main()
