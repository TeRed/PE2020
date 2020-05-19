import unittest
from logger_connector import LoggerConnector
from article_logs import ArticleLogs
from log import Log
from config_manager import ConfigManager


class MyTestCase(unittest.TestCase):
    def test_get_all_logs(self):
        # Given
        config_manager = ConfigManager()
        config_manager.logger_path = 'test_logger.json'
        logger = LoggerConnector(config_manager)
        expected = [
            ArticleLogs('1', [Log("1", "08-05-2020", "Zapisano")]),
            ArticleLogs('2', [Log("1", "08-05-2020", "Zapisano"), Log("2", "07-05-2020", "Usunięto")])
        ]

        # When
        logs = logger.get_all_logs()

        # Then
        self.assertListEqual(expected, logs)

    def test_get_logs_by_id(self):
        # Given
        config_manager = ConfigManager()
        config_manager.logger_path = 'test_logger.json'
        logger = LoggerConnector(config_manager)
        article_id = '1'
        expected = [ArticleLogs('1', [Log("1", "08-05-2020", "Zapisano")])]

        # When
        logs = logger.get_logs_by_id(article_id)

        # Then
        self.assertListEqual(expected, logs)


if __name__ == '__main__':
    unittest.main()
