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
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db_file_connector = DbFileConnector(config_manager)
        db = DBConnector(db_file_connector)

        expected = [
            Article('1', ["mlotek", "hammer"], True),
            Article('2', ["wiertarka", "driller"], False)
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
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_string = 'rka'
        expected = [Article('2', ["wiertarka", "driller"], False)]

        # When
        articles = db.get_articles_by_name(search_string)

        # Then
        self.assertListEqual(expected, articles)

    def test_get_articles_by_name_2(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False}
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
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False},
            {"id": "3", "name": ["wiertarka2", "driller2"], "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        available = False
        expected = [
            Article('2',["wiertarka", "driller"] , False),
            Article('3',["wiertarka2", "driller2"] , False)
        ]

        # When
        articles = db.get_articles_by_availability(available)

        # Then
        self.assertListEqual(expected, articles)

    def test_get_article_by_id(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False},
            {"id": "3", "name": ["wiertarka2", "driller2"], "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2',["wiertarka", "driller"] , False)

        # When
        article = db.get_article_by_id(search_id)

        # Then
        self.assertEqual(expected, article)

    def test_get_article_by_id_2(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False}
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

        article = Article('1', ["mlotek", "hammer"], False)
        expected = [Article('1', ["mlotek", "hammer"], False)]

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

        article = Article('1', ["mlotek", "hammer"], False)
        article2 = Article('1', ["mlotek2", "hammer2"], False)
        expected = [Article('1', ["mlotek", "hammer"], False)]

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

        article = Article('1', ["mlotek", "hammer"], False)
        article2 = Article('2', ["mlotek2", "hammer2"], False)
        expected = [Article('1', ["mlotek", "hammer"], False), Article('2', ["mlotek2", "hammer2"], False)]

        # When
        db.add_article(article)
        db.add_article(article)
        db.add_article(article2)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_remove_article_by_id(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True}
        ]

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
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        article_id = '2'
        expected = [Article('1', ["mlotek", "hammer"], True)]

        # When
        db.remove_article_by_id(article_id)

        # Then
        self.assertListEqual(expected, db.get_all_articles())

    def test_change_article_availability(self):
        # Given
        articles = [
            {"id": "1", "name": ["mlotek", "hammer"], "is_available": True},
            {"id": "2", "name": ["wiertarka", "driller"], "is_available": False}
        ]

        with open(self.config_file_name, "w") as f:
            json.dump(articles, f)

        config_manager = ConfigManager()
        config_manager.db_path = self.config_file_name
        db = DBConnector(DbFileConnector(config_manager))

        search_id = '2'
        expected = Article('2',["wiertarka", "driller"], True)

        # When
        article = db.change_article_availability(search_id, True)

        # Then
        self.assertEqual(expected, article)


if __name__ == '__main__':
    unittest.main()
