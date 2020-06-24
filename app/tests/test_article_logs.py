import unittest
from article_logs import ArticleLogs
from log import Log


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        obj = ArticleLogs('1', [Log("08-05-2020", "Added")])
        expected = '''
            {
                "id": "1",
                "logs": [
                  {
                    "data": "08-05-2020",
                    "text": "Added"
                  }
                ]
            }
        '''

        # When
        actual = str(obj)

        # Then
        self.assertCountEqual(
            ''.join(expected.split()),
            ''.join(actual.split())
        )

    def test_article_serialization2(self):
        # Given
        obj = ArticleLogs('2', [Log("11-07-2041", "Deleted")])
        expected = '''
            {
                "id": "2",
                "logs": [
                  {
                    "data": "11-07-2041",
                    "text": "Deleted"
                  }
                ]
            }
        '''

        # When
        actual = str(obj)

        # Then
        self.assertCountEqual(
            ''.join(expected.split()),
            ''.join(actual.split())
        )

if __name__ == '__main__':
    unittest.main()
