import unittest
from log import Log


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        obj = Log("08-05-2020", "Added")
        expected = '''
        {
            "data": "08-05-2020",
            "text": "Added"
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
