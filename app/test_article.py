import unittest
import article


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        obj = article.Article('1', 'Test', 2, 2, True)
        expected = '''
        {
            "id": "1",
            "is_available": true,
            "name": "Test",
            "quantity": 2,
            "total_quantity": 2
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
