import unittest
import article_logs
from log import Log


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        obj = article_logs.ArticleLogs('1', [ Log("1", "08-05-2020", "Zapisano") ])
        expected = '''
            {
            "id": "1",
            "logs": [
              {
                "id": "1",
                "data": "08-05-2020",
                "text": "Zapisano"
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
