import json
import unittest
from io import StringIO
from os import remove
from unittest import mock

from unittest.mock import patch

from article import Article
from config_manager import ConfigManager
from db_connector import DBConnector
from file_connector import LoggerFileConnector, DbFileConnector
from interface import Invoker, AppInfoLogger
from logger_connector import LoggerConnector


class MyTestCase(unittest.TestCase):
    database_file_name = 'test_interface_database.json'
    logger_file_name = 'test_interface_logger.json'
    config_file_name = "test_interface_config.json"

    def setUp(self):
        open(self.database_file_name, "w").close()
        open(self.logger_file_name, "w").close()
        open(self.config_file_name, "w").close()

    def tearDown(self):
        remove(self.database_file_name)
        remove(self.logger_file_name)
        remove(self.config_file_name)

    def test_display_all_articles_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name

        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 20, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 30, "quantity": 5, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |   NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 1  |  hammer |      mlotek      |       20       |    2     |     YES      |" + "\n" \
                   + "| 2  | driller |    wiertarka     |       30       |    5     |      NO      |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            with mock.patch('builtins.input', return_value="1"):
                INVOKER.execute('1')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_borrowed_articles_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name

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

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

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
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)
        logs = [{'id': '1', 'logs': [{"data": "08-05-2020","text": "Returned 1"}]}]

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = "+----+------------+------------+" + "\n" \
                   + "| ID |    DATE    |    TEXT    |" + "\n" \
                   + "+----+------------+------------+" + "\n" \
                   + "| 1  | 08-05-2020 | 1 RETURNED |" + "\n" \
                   + "+----+------------+------------+"

        # When
        with patch('sys.stdout', new=StringIO()) as result:
            with mock.patch('builtins.input', return_value="2"):
                INVOKER.execute('3')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_display_history_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        logs = [{'id': '1', 'logs': [{"data": "12-11-2020", "text": "Returned 1"}]}]

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = "+------------+------------+" + "\n" \
                   + "|    DATE    |    TEXT    |" + "\n" \
                   + "+------------+------------+" + "\n" \
                   + "| 12-11-2020 | 1 RETURNED |" + "\n" \
                   + "+------------+------------+"

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('4')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_add_article_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name

        logs = [
            {'id': '1', 'logs': [{"data": "08-05-2020", "text": "Returned 1"}]},
            {'id': '2', 'logs': [{"data": "08-05-2020", "text": "Borrowed 1"}, {"data": "07-05-2020", "text": "Deleted"}]}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump([], f)

        with open(self.logger_file_name, "w") as f:
            json.dump(logs, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = [Article('3', ["szalik", "scarf"], 1, 1, True)]

        # When
        with mock.patch('builtins.input', side_effect=["scarf", "szalik", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('5')

        self.assertEqual(expected,  db.get_articles_by_name('scarf'))

    def test_delete_article_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:  # rozroznienie na pliki db i loggera
            json.dump([], f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        # When
        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('6')

        # Then
        self.assertEqual(db.get_article_by_id("1"), False)

    def test_search_for_an_article_by_name_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| ID |   NAME  | NAME_SECOND_LANG | TOTAL_QUANTITY | QUANTITY | AVAILABILITY |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+" + "\n" \
                   + "| 2  | driller |    wiertarka     |       2        |    2     |      NO      |" + "\n" \
                   + "+----+---------+------------------+----------------+----------+--------------+"

        # When
        with mock.patch('builtins.input', return_value="dri"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('7')

        # Then
        self.assertEqual(expected, result.getvalue())

    def test_search_for_an_article_by_id_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

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
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "3", "is_available": True,"name": ["Szalik","Scarf"],"quantity": 1,"total_quantity": 1}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = [Article('3', ["Szalik", "Scarf"], 1, 1, False)]

        # When
        with mock.patch('builtins.input', side_effect=["3", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('9')

        self.assertEqual(str(expected[0]), str(db.get_articles_by_name('szalik')[0]))

    def test_display_config_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

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
        config = {'db_path': 'db.json', 'language': 'en', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)

        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        config = {'db_path': 'db.json', 'language': 'en', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

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
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name

        config = {'db_path': 'db.json', 'language': 'pl', 'logger_path': 'logger.json'}
        with open(self.config_file_name, "w") as f:
            json.dump(config, f)
        config_manager = ConfigManager(self.config_file_name)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = "INFO: CONFIGURATION_SAVED\n"

        with mock.patch('builtins.input', return_value="1"):
            with patch('sys.stdout', new=StringIO()) as result:
                INVOKER.execute('12')

        # Then
        self.assertEqual(result.getvalue(), expected)



    def test_borrow_article_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)


        # When
        with mock.patch('builtins.input', side_effect=["1", "1", "1"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('13')

        # Then
        expected = [Article('1', ["mlotek", "hammer"], 2, 1, True)]
        self.assertEqual(str(expected[0]), str(db.get_articles_by_name('mlotek')[0]))

    def test_borrow_article_command2(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name

        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 4, "quantity": 1, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        # When
        with mock.patch('builtins.input', side_effect=["1", "2", "\n"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('13')

        # Then
        expected = [Article('1', ["mlotek", "hammer"], 4, 1 , True)]
        self.assertEqual(str(expected[0]), str(db.get_articles_by_name('mlotek')[0]))

    def test_return_article_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "18", "is_available": True, "name": ["Paczka", "Package"], "quantity": 150, "total_quantity": 250}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = [Article('18', ["Paczka", "Package"], 250, 250, True)]

        # When
        with mock.patch('builtins.input', side_effect=["18", "100", "\n"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('14')

        # Then
        self.assertEqual(str(expected[0]), str(db.get_articles_by_name('Paczka')[0]))

    def test_return_article_command_2(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name

        articles = [
            {"id": "18", "is_available": True, "name": ["Paczka", "Package"], "quantity": 150, "total_quantity": 250}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        with open(self.logger_file_name, "w") as f:
            json.dump([], f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

        expected = [Article('18', ["Paczka", "Package"], 250, 150, True)]

        # When
        with mock.patch('builtins.input', side_effect=["18", "101", "\n"]):
            with patch('sys.stdout', new=StringIO()):
                INVOKER.execute('14')

        # Then
        self.assertEqual(str(expected[0]), str(db.get_articles_by_name('Paczka')[0]))

    def test_display_all_available_articles_command(self):
        # Given
        config_manager = ConfigManager()
        app_info_logger = AppInfoLogger()
        db = DBConnector(DbFileConnector(config_manager))
        logger = LoggerConnector(LoggerFileConnector(config_manager))
        config_manager.db_path = self.database_file_name
        config_manager.logger_path = self.logger_file_name
        
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.database_file_name, "w") as f:
            json.dump(articles, f)

        INVOKER = Invoker(db, logger, config_manager, app_info_logger)

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
