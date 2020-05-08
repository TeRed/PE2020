import unittest
from app.logger_connector import LoggerConnector
from app.article_logs import ArticleLogs
from app.log import Log


class MyTestCase(unittest.TestCase):
    def test_get_all_logs(self):
        # Given
        logger = LoggerConnector('test_logger.json')
        expected = [
            ArticleLogs('1', [Log("1", "08-05-2020", "Zapisano")]),
            ArticleLogs('2', [Log("1", "08-05-2020", "Zapisano"), Log("2", "07-05-2020", "Usunięto")])
        ]

        # When
        logs = logger.get_all_logs()

        # Then
        self.assertListEqual(expected, logs)

    def test_get_articles_by_name(self):
        # Given
        logger = LoggerConnector('test_logger.json')
        article_id = '1'
        expected = [ArticleLogs('1', [Log("1", "08-05-2020", "Zapisano")])]

        # When
        logs = logger.get_logs_by_id(article_id)

        # Then
        self.assertListEqual(expected, logs)


if __name__ == '__main__':
    unittest.main()
