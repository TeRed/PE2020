import unittest
from db_connector import DBConnector
from article import Article


class MyTestCase(unittest.TestCase):
    def test_get_all_articles(self):
        # Given
        db = DBConnector('test_db.json')
        expected = [
            Article('1', 'Test', True),
            Article('2', 'Test2', False)
        ]

        # When
        articles = db.get_all_articles()

        # Then
        self.assertListEqual(expected, articles)

    def test_get_articles_by_name(self):
        # Given
        db = DBConnector('test_db.json')
        search_string = 'eSt2'
        expected = [Article('2', "Test2", False)]

        # When
        articles = db.get_articles_by_name(search_string)

        # Then
        self.assertListEqual(expected, articles)

    def test_change_article_availability(self):
        # Given
        db = DBConnector('test_db.json')
        id = '2'
        availability = True
        expected = Article('2', "Test2", True)

        # When
        article = db.change_article_availability(id, True)

        # Then
        self.assertEqual(expected, article)

if __name__ == '__main__':
    unittest.main()
