import unittest
from app import article


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        obj = article.Article('1', 'Test', True)
        expected = '''
        {
            "id": "1",
            "is_available": true,
            "name": "Test"
        }
        '''

        # When
        actual = str(obj)

        # Then
        self.assertEqual(
            ''.join(expected.split()),
            ''.join(actual.split())
        )


if __name__ == '__main__':
    unittest.main()
