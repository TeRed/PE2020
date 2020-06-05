import unittest
import json
from db_connector import DBConnector
from article import Article
from config_manager import ConfigManager
from os import remove
from file_connector import DbFileConnector


class MyTestCase(unittest.TestCase):

    config_file_name = 'test_db.json'

    def setUp(self):
        open(self.config_file_name, "w").close()

    def tearDown(self):
        remove(self.config_file_name)

    def test_singleton(self):
        # Given
        config_manager = ConfigManager()
        config_manager.logger_path = self.config_file_name

        # When
        db = DBConnector(DbFileConnector(config_manager))
        db2 = DBConnector(DbFileConnector(config_manager))

        # Then
        self.assertEqual(db2, db)

    def test_get_all_articles(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db_file_connector = DbFileConnector(config_manager)
        db = DBConnector(db_file_connector)

        expected = [
            Article('1', 'Test', True),
            Article('2', 'Test2', False)
        ]

        # When
        articles = db.get_all_articles()

        # Then
        self.assertListEqual(expected, articles)

    def test_get_all_articles_2(self):
        # Given
        articles = []

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db_file_connector = DbFileConnector(config_manager)
        db = DBConnector(db_file_connector)

        expected = []

        # When
        articles = db.get_all_articles()

        # Then
        self.assertListEqual(expected, articles)

    def test_get_articles_by_name(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_string = 'eSt2'
        expected = [Article('2', "Test2", False)]

        # When
        articles = db.get_articles_by_name(search_string)

        # Then
        self.assertListEqual(expected, articles)

    def test_get_articles_by_name_2(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_string = 'Missing'
        expected = []

        # When
        articles = db.get_articles_by_name(search_string)

        # Then
        self.assertListEqual(expected, articles)

    def test_get_article_by_id(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2', "Test2", False)

        # When
        article = db.get_article_by_id(search_id)

        # Then
        self.assertEqual(expected, article)

    def test_get_article_by_id_2(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '3'
        expected = False

        # When
        article = db.get_article_by_id(search_id)

        # Then
        self.assertEqual(expected, article)

    def test_add_article(self):
        # Given
        articles = []

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        article = Article('1', "Test", False)
        expected = [Article('1', "Test", False)]

        # When
        db.add_article(article)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_remove_article_by_id(self):
        # Given
        articles = [{"id": "1", "name": "Test", "is_available": False}]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        article_id = '1'
        expected = []

        # When
        db.remove_article_by_id(article_id)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_change_article_availability(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "is_available": True},
            {"id": "2", "name": "Test2", "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2', "Test2", True)

        # When
        article = db.change_article_availability(search_id, True)

        # Then
        self.assertEqual(expected, article)


if __name__ == '__main__':
    unittest.main()
