import unittest
from string_calculator import StringCalculator


class TestStringCalculator(unittest.TestCase):

    def test_add_up_to_two_numbers(self):
        # Test add func in calculator with up to 2 numbers in string
        calculator = StringCalculator()

        self.assertEqual(calculator.add(""), 0)
        self.assertEqual(calculator.add("1"), 1)
        self.assertEqual(calculator.add("1,2"), 1 + 2)

    def test_add_all_numbers(self):
        # Test add func in calculator with unknow amount of numbers in string
        calculator = StringCalculator()

        self.assertEqual(calculator.add("1,2,3,4,5"), 15)
        self.assertEqual(calculator.add("1,2,3,4,5,10,60,20"), 105)

    def test_add_allow_new_line(self):
        # Test add func in calculator with new line as separator
        calculator = StringCalculator()

        self.assertEqual(calculator.add("1\n2,3"), 6)
        self.assertEqual(calculator.add("1,2\n3,4\n5"), 15)
        self.assertEqual(calculator.add("1,2\n3,4,5\n10,60\n20"), 105)

    def test_add_specified_delimiter(self):
        # Test add func in calculator with new line as separator
        calculator = StringCalculator()

        self.assertEqual(calculator.add("//;\n1;2"), 3)
        self.assertEqual(calculator.add("1,2\n3,4\n5"), 15)

    def test_add_negative_exception(self):
        # Test add func in calculator, should throw exception when exist negative numbers
        calculator = StringCalculator()

        with self.assertRaises(ValueError) as context:
            calculator.add("1,2,-1")

        self.assertTrue('Negatives not allowed: -1' in str(context.exception))

    def test_add_number_bigger_than_100(self):
        # Test add func in calculator, should not add number bigger than 1000
        calculator = StringCalculator()

        self.assertEqual(calculator.add('1,2,1001'), 3)
        self.assertEqual(calculator.add('2000,1001,4321'), 0)

    def test_add_long_than_one_char_delimiter(self):
        # Test add func in calculator, should allow delimiter longer than one char
        calculator = StringCalculator()

        self.assertEqual(calculator.add('//[***]\n1***2***3'), 6)
        self.assertEqual(calculator.add('//[,,]\n2000,,1001,,4321'), 0)

    def test_add_multiple_delimiters(self):
        # Test add func in calculator, should allow delimiter longer than one char
        calculator = StringCalculator()

        self.assertEqual(calculator.add('//[*][%]\n1*2%3'), 6)
        self.assertEqual(calculator.add('//[*][%]\n1*2'), 3)

    def test_add_multiple_long_delimiters(self):
        # Test add func in calculator, should allow delimiter longer than one char
        calculator = StringCalculator()

        self.assertEqual(calculator.add('//[***][$$$]\n1***2$$$3'), 6)


if __name__ == '__main__':
    unittest.main()
