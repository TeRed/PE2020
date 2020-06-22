import json
import unittest
from io import StringIO
from os import remove
from unittest import mock

from unittest.mock import patch

from app.config_manager import ConfigManager
from app.db_connector import DBConnector
from app.file_connector import LoggerFileConnector, DbFileConnector
from app.interface import Invoker, AppInfoLogger
from app.logger_connector import LoggerConnector


class MyTestCase(unittest.TestCase):
    database_file_name = 'test_interface.json'
    logger_file_name = 'test_interface_logger.json'
    config_manager = ConfigManager()
    db_file_connector = DbFileConnector(config_manager)
    logger = LoggerConnector(LoggerFileConnector(config_manager))
    app_info_logger = AppInfoLogger()
    db = DBConnector(db_file_connector)

    def setUp(self):
        open(self.database_file_name, "w").close()
        open(self.logger_file_name, "w").close()
        self.config_manager.db_path = self.database_file_name
        self.config_manager.logger_path = self.logger_file_name

    def tearDown(self):
        remove(self.database_file_name)
        remove(self.logger_file_name)

    def test_display_all_articles_command(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+-------+--------------+" + "\n" \
                   + "| ID |  NAME | AVAILABILITY |" + "\n" \
                   + "+----+-------+--------------+" + "\n" \
                   + "| 1  |  Test |     YES      |" + "\n" \
                   + "| 2  | Test2 |      NO      |" + "\n" \
                   + "+----+-------+--------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            INVOKER.execute('1')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_borrowed_articles_command(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+-------+--------------+" + "\n" \
                   + "| ID |  NAME | AVAILABILITY |" + "\n" \
                   + "+----+-------+--------------+" + "\n" \
                   + "| 2  | Test2 |      NO      |" + "\n" \
                   + "+----+-------+--------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            INVOKER.execute('2')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_full_history_command(self):
        # Given
        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Returned"}]},
            {'id': '2', 'logs': [{"data": "08-05-2020", "text": "Borrowed"}, {"data": "07-05-2020", "text": "Deleted"}]}
        ]

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+------------+----------+" + "\n" \
                   + "| ID |    DATE    |   TEXT   |" + "\n" \
                   + "+----+------------+----------+" + "\n" \
                   + "| 1  | 08-05-2020 | RETURNED |" + "\n" \
                   + "| 2  | 08-05-2020 | BORROWED |" + "\n" \
                   + "+----+------------+----------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            INVOKER.execute('3')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_history_command(self):
        # Given
        logs = [{'id': '1', 'logs': [{"data": "08-05-2020", "text": "Returned"}]}]

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+------------+----------+" + "\n" \
                   + "|    DATE    |   TEXT   |" + "\n" \
                   + "+------------+----------+" + "\n" \
                   + "| 08-05-2020 | RETURNED |" + "\n" \
                   + "+------------+----------+"

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('4')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_add_article_command(self):
        # Given
        articles = []

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "Dodano nowy artykuł\n"

        # When
        with mock.patch('builtins.input', return_value="11"):
            with mock.patch('builtins.input', return_value="Apaszka"):
                with patch('sys.stdout', new=StringIO()) as result:
                    INVOKER.execute('5')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_delete_article_command(self):
        # Given
        articles = [{"id": "1", "name": "Test", "is_available": False}]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:  # rozroznienie na pliki db i loggera
            json.dump([], f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "INFO: ARTICLE_DELETED\n"

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('6')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_search_for_an_article_by_name_command(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+-------+--------------+" + "\n" \
                   + "| ID |  NAME | AVAILABILITY |" + "\n" \
                   + "+----+-------+--------------+" + "\n" \
                   + "| 2  | Test2 |      NO      |" + "\n" \
                   + "+----+-------+--------------+"

        # When
        with mock.patch('builtins.input', return_value="eSt2"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('7')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_search_for_an_article_by_id_command(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+-------+--------------+" + "\n" \
                   + "| ID |  NAME | AVAILABILITY |" + "\n" \
                   + "+----+-------+--------------+" + "\n" \
                   + "| 2  | Test2 |      NO      |" + "\n" \
                   + "+----+-------+--------------+"

        # When
        with mock.patch('builtins.input', return_value="2"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('8')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_change_status_command(self):  # add logger?
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "2 	 Test2 	 False\n"

        # When
        with mock.patch('builtins.input', return_value="2"):
            with mock.patch('builtins.input', return_value="1"):
                with patch('sys.stdout', new=StringIO()) as result:
                    INVOKER.execute('9')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_config_command(self):
        # Given
        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "Aktualna konfiguracja:\n" + "db_path: \"test_interface.json\"" + "\n" + "logger_path: \"test_interface_logger.json\"" + "\n"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            INVOKER.execute('10')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_change_config_command(self):
        # Given
        config = {'db_path': 'db.json', 'logger_path': 'logger.json'}
        with open(self.database_file_name, "w") as f:
            json.dump(config, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "Zmiana konfiguracji" + "\n" + "1: \"db_path\"" + "\n" + "2: \"logger_path\"" + "\n" + "Atrybut został zmieniony!\n"

        # When
        with mock.patch('builtins.input', return_value="db_path"):
            with mock.patch('builtins.input', return_value="0"):
                with patch('sys.stdout', new=StringIO()) as result:
                    INVOKER.execute('11')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_save_config_command(self):
        # Given
        config = {'db_path': 'db.json', 'logger_path': 'logger.json'}
        with open(self.database_file_name, "w") as f:
            json.dump(config, f)

        # When
        config_manager = ConfigManager(self.database_file_name)
        config_attributes = list()

        for key, val in config_manager.__dict__.items():
            config_attributes.append(key)
        setattr(config_manager, config_attributes[0], 'db2.json')
        config_manager.save_configuration(self.database_file_name)

        # Then
        with open(self.database_file_name) as f:
            config = json.load(f)

        self.assertEqual(config['db_path'], 'db2.json')


if __name__ == '__main__':
    unittest.main()
