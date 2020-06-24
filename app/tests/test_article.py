import unittest
import article


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        name1 = 'mlotek'
        name2 = 'hammer'
        obj = article.Article('1', [name1,name2], 2, 2, True)
        expected = '''
        {
            "id": "1",
            "is_available": true,
            "name": ["mlotek", "hammer"],
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

    def test_article_serialization2(self):
        # Given
        name1 = ''
        name2 = 'hammer'
        obj = article.Article('4', [name1,name2], 6, 5, False)
        expected = '''
        {
            "id": "4",
            "is_available": false,
            "name": ["", "hammer"],
            "quantity": 5,
            "total_quantity": 6
        }
        '''

        # When
        actual = str(obj)

        # Then
        self.assertEqual(
            ''.join(expected.split()),
            ''.join(actual.split())
        )
    def test_article_serialization_fail(self):
        # Given
        name1 = 'mlotek'
        name2 = 'hammer'
        obj = article.Article('1', [name1,name2], 2, 2, False)
        expected = '''
        {
            "id": "1",
            "is_available": true,
            "name": ["mlotek", "hammer"],
            "quantity": 2,
            "total_quantity": 2
        }
        '''

        # When
        actual = str(obj)

        # Then
        self.assertNotEqual(
            ''.join(expected.split()),
            ''.join(actual.split())
        )


if __name__ == '__main__':
    unittest.main()
