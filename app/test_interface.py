import json
import unittest
from io import StringIO
from os import remove
from unittest import mock

from unittest.mock import patch

from article import Article
from app.config_manager import ConfigManager
from app.db_connector import DBConnector
from app.file_connector import LoggerFileConnector, DbFileConnector
from app.interface import Invoker, AppInfoLogger
from app.logger_connector import LoggerConnector


class MyTestCase(unittest.TestCase):
    database_file_name = 'test_interface_database.json'
    logger_file_name = 'test_interface_logger.json'
    config_file_name = "test_interface_config.json"
    config_manager = ConfigManager()
    db_file_connector = DbFileConnector(config_manager)
    logger = LoggerConnector(LoggerFileConnector(config_manager))
    app_info_logger = AppInfoLogger()
    db = DBConnector(db_file_connector)

    def setUp(self):
        open(self.database_file_name, "w").close()
        open(self.logger_file_name, "w").close()
        open(self.config_file_name, "w").close()
        self.config_manager.db_path = self.database_file_name
        self.config_manager.logger_path = self.logger_file_name

    def tearDown(self):
        remove(self.database_file_name)
        remove(self.logger_file_name)
        remove(self.config_file_name)

    def test_display_all_articles_command(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |   NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 1  |  hammer |      mlotek      |       2        |    2     |     YES      |" + "\n" \
                   + "| 2  | driller |    wiertarka     |       2        |    2     |      NO      |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            with mock.patch('builtins.input', return_value="1"):
                INVOKER.execute('1')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_borrowed_articles_command(self):
        # Given
        articles = [
            {"id": "18", "is_available": True, "name": ["Paczka", "Package"], "quantity": 150, "total_quantity": 250}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        logs = [
            {"id": "18",
             "logs": [{"data": "2020-06-22", "text": "Added"}, {"data": "2020-06-22", "text": "Borrowed 100"}]}
        ]

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |   NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 18 | Package |      Paczka      |      250       |   150    |     YES      |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            with mock.patch('builtins.input', return_value="1"):
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

        expected = "+----+------------+-------------------+" + "\n" \
                   + "| ID |    DATE    |        TEXT       |" + "\n" \
                   + "+----+------------+-------------------+" + "\n" \
                   + "| 1  | 08-05-2020 | Returned RETURNED |" + "\n" \
                   + "| 2  | 08-05-2020 | Borrowed BORROWED |" + "\n" \
                   + "+----+------------+-------------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            with mock.patch('builtins.input', return_value="2"):
                INVOKER.execute('3')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_history_command(self):
        # Given
        logs = [{'id': '1', 'logs': [{"data": "08-05-2020", "text": "Returned"}]}]

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+------------+-------------------+" + "\n" \
                   + "|    DATE    |        TEXT       |" + "\n" \
                   + "+------------+-------------------+" + "\n" \
                   + "| 08-05-2020 | Returned RETURNED |" + "\n" \
                   + "+------------+-------------------+"

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('4')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_add_article_command(self):  # dodaje poprawnie, czy sprawdzac w bazie np?
        # Given

        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Returned"}]},
            {'id': '2', 'logs': [{"data": "08-05-2020", "text": "Borrowed"}, {"data": "07-05-2020", "text": "Deleted"}]}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump([], f)

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = [Article('3', ["szalik", "scarf"], 1, 1, True)]

        # When
        with mock.patch('builtins.input', side_effect=["scarf", "szalik", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('5')

        self.assertEqual(expected,  self.db.get_articles_by_name('scarf'))

    def test_delete_article_command(self):
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:  # rozroznienie na pliki db i loggera
            json.dump([], f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('6')

        # Then
        self.assertEqual(self.db.get_article_by_id("1"), False)

    def test_search_for_an_article_by_name_command(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |   NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 2  | driller |    wiertarka     |       2        |    2     |      NO      |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+"

        # When
        with mock.patch('builtins.input', return_value="driller"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('7')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_search_for_an_article_by_id_command(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |   NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 2  | driller |    wiertarka     |       2        |    2     |      NO      |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+"

        # When
        with mock.patch('builtins.input', return_value="2"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('8')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_change_status_command(self):

        # Given
        articles = [
            {"id": "3", "is_available": True,"name": ["Szalik","Scarf"],"quantity": 1,"total_quantity": 1}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = [Article('3', ["Szalik", "Scarf"], 1, 1, False)]

        # When
        with mock.patch('builtins.input', side_effect=["3", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('9')

        self.assertEqual(str(expected[0]), str(self.db.get_articles_by_name('szalik')[0]))

    def test_display_config_command(self):
        # Given
        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "CURRENT_CONFIGURATION" + "\n" \
                   + "language: \"en\"" + "\n" \
                   + "db_path: \"test_interface_database.json\"" + "\n" \
                   + "logger_path: \"test_interface_logger.json\"" + "\n"

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('10')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_change_config_command(self):
        # Given
        config = {'db_path': 'db.json', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "CONFIGURATION_CHANGE" + "\n" \
                   + "1: \"language\"" + "\n" \
                   + "2: \"db_path\"" + "\n" \
                   + "3: \"logger_path\"" + "\n" \
                   + "INFO: NO_SUCH_ATTRIBUTE\n"

        # When
        with mock.patch('builtins.input', return_value="db_path"):
            with mock.patch('builtins.input', return_value="0"):
                with patch('sys.stdout', new=StringIO()) as result:
                    INVOKER.execute('11')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_save_config_command(self):
        # Given
        config = {'db_path': 'db.json', 'language': 'pl', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)
        config_manager = ConfigManager(self.config_file_name)

        INVOKER = Invoker(self.db, self.logger, config_manager, self.app_info_logger)

        expected = "INFO: CONFIGURATION_SAVED\n"

        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('12')

        # Then
        self.assertEqual(result.getvalue(), expected)

    def test_borrow_article_command(self):
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)


        # When
        with mock.patch('builtins.input', side_effect=["1", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('13')

        # Then
        expected = [Article('1', ["mlotek", "hammer"], 2, 1, True)]
        self.assertEqual(str(expected[0]), str(self.db.get_articles_by_name('mlotek')[0]))

    def test_return_article_command(self):
        articles = [
            {"id": "18", "is_available": True, "name": ["Paczka", "Package"], "quantity": 150, "total_quantity": 250}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = [Article('18', ["Paczka", "Package"], 250, 151, True)]

        # When
        with mock.patch('builtins.input', side_effect=["18", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('14')

        # Then
        self.assertEqual(str(expected[0]), str(self.db.get_articles_by_name('Paczka')[0]))

    def test_display_all_available_articles_command(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(self.db, self.logger, self.config_manager, self.app_info_logger)

        expected = "+----+--------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |  NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+--------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 1  | hammer |      mlotek      |       2        |    2     |     YES      |" + "\n" \
                   + "+----+--------+------------------+----------------+----------+--------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            with mock.patch('builtins.input', return_value="1"):
                INVOKER.execute('15')

        # Then
        self.assertEqual(expected, result.getvalue())


if __name__ == '__main__':
    unittest.main()
