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
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db_file_connector = DbFileConnector(config_manager)
        db = DBConnector(db_file_connector)

        expected = [
            Article('1', 'Test', 2, 2, True),
            Article('2', 'Test2', 2, 2, False)
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
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_string = 'eSt2'
        expected = [Article('2', "Test2", 2, 2, False)]

        # When
        articles = db.get_articles_by_name(search_string)

        # Then
        self.assertListEqual(expected, articles)

    def test_get_articles_by_name_2(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2,"is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False}
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

    def test_get_articles_by_availability(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False},
            {"id": "3", "name": "Test3", "total_quantity": 4, "quantity": 4, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        available = False
        expected = [
            Article('2', 'Test2', 2, 2, False),
            Article('3', 'Test3', 4, 4, False)
        ]

        # When
        articles = db.get_articles_by_availability(available)

        # Then
        self.assertListEqual(expected, articles)

    def test_get_article_by_id(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2,"is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2', "Test2", 2, 2, False)

        # When
        article = db.get_article_by_id(search_id)

        # Then
        self.assertEqual(expected, article)

    def test_get_article_by_id_2(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False}
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

        article = Article('1', "Test", 2, 2, False)
        expected = [Article('1', "Test", 2, 2, False)]

        # When
        db.add_article(article)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_add_article_2(self):
        # Given
        articles = []

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        article = Article('1', "Test", 2, 2, False)
        article2 = Article('1', "Test2", 2, 2, False)
        expected = [Article('1', "Test", 2, 2, False)]

        # When
        db.add_article(article)
        db.add_article(article)
        db.add_article(article2)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_add_article_3(self):
        # Given
        articles = []

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        article = Article('1', "Test", 2, 2, False)
        article2 = Article('2', "Test2", 2, 2, False)
        expected = [Article('1', "Test", 2, 2, False), Article('2', "Test2", 2, 2, False)]

        # When
        db.add_article(article)
        db.add_article(article)
        db.add_article(article2)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_remove_article_by_id(self):
        # Given
        articles = [{"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": False}]

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

    def test_remove_article_by_id_2(self):
        # Given
        articles = [{"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": False}]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        article_id = '2'
        expected = [Article('1', "Test", 2, 2, False)]

        # When
        db.remove_article_by_id(article_id)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_change_article_availability(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 2, "quantity": 2, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2', "Test2", 2, 2, True)

        # When
        article = db.change_article_availability(search_id, True)

        # Then
        self.assertEqual(expected, article)

    def test_add_article_quantity(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 22, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 22, "quantity": 2, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2', "Test2", 22, 22, True)
        search_id_2 = '1'
        expected_2 = Article('1', "Test", 22, 12, True)

        # When
        article = db.add_article_quantity(search_id, 20, True)
        article_2 = db.add_article_quantity(search_id_2, 10, True)

        # Then
        self.assertEqual(expected, article)
        self.assertEqual(expected_2, article_2)

    def test_get_articles_by_borrowed(self):
        # Given
        articles = [
            {"id": "1", "name": "Test", "total_quantity": 2, "quantity": 2, "is_available": True},
            {"id": "2", "name": "Test2", "total_quantity": 3, "quantity": 2, "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        expected = Article("2", "Test2", 3, 2, False)

        # When
        article = db.get_articles_by_borrowed()[0]

        # Then
        self.assertEqual(expected, article)



if __name__ == '__main__':
    unittest.main()
