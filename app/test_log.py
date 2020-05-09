import unittest
import log


class MyTestCase(unittest.TestCase):
    def test_article_serialization(self):
        # Given
        obj = log.Log("1", "08-05-2020", "Zapisano")
        expected = '''
        {
            "id": "1",
            "data": "08-05-2020",
            "text": "Zapisano"
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
