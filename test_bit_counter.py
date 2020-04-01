from unittest import TestCase
from bit_counter import BitCounter


class TestBitCounter(TestCase):
    # A
    def test_no_of_bits_1(self):
        # Arrange
        counter = BitCounter()
        number_string = ""
        expected_result = 0

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    def test_no_of_bits_2(self):
        # Arrange
        counter = BitCounter()
        number_string = "0"
        expected_result = 0

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    def test_no_of_bits_3(self):
        # Arrange
        counter = BitCounter()
        number_string = "35"
        expected_result = 3

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    def test_no_of_bits_4(self):
        # Arrange
        counter = BitCounter()
        number_string = "255"
        expected_result = 8

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    # B
    def test_no_of_bits_out_of_range(self):
        counter = BitCounter()

        with self.assertRaises(Exception) as context:
            counter.no_of_bits("300")

        self.assertTrue('Number out of range.' in str(context.exception))

    def test_no_of_bits_out_of_range_2(self):
        counter = BitCounter()

        with self.assertRaises(Exception) as context:
            counter.no_of_bits("-1")

        self.assertTrue('Number out of range.' in str(context.exception))

    # C
    def test_no_of_bits_many_numbers(self):
        # Arrange
        counter = BitCounter()
        number_string = "35;1"
        expected_result = 4

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    def test_no_of_bits_many_numbers_2(self):
        # Arrange
        counter = BitCounter()
        number_string = "35;1;0;3"
        expected_result = 6

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    # D
    def test_no_of_bits_whitespaces_delimiters(self):
        # Arrange
        counter = BitCounter()
        number_string = "35 1;0 3"
        expected_result = 6

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    # E
    def test_no_of_bit_whitespaces_delimiters_2(self):
        # Arrange
        counter = BitCounter()
        number_string = "1\t1;1\t\t\n1\n1 1"
        expected_result = 6

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    # F
    def test_no_of_bits_wrong_delimiter(self):
        counter = BitCounter()

        with self.assertRaises(Exception) as context:
            counter.no_of_bits("35|18")

        self.assertTrue('String contains illegal characters.' in str(context.exception))

    def test_no_of_bits_wrong_delimiter_2(self):
        counter = BitCounter()

        with self.assertRaises(Exception) as context:
            counter.no_of_bits("35&18")

        self.assertTrue('String contains illegal characters.' in str(context.exception))

    # G
    def test_no_of_bits_hex(self):
        # Arrange
        counter = BitCounter()
        number_string = "$ff"
        expected_result = 8

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)

    def test_no_of_bits_many_hex(self):
        # Arrange
        counter = BitCounter()
        number_string = "$ff\t1;$5A"
        expected_result = 13

        # Act
        result = counter.no_of_bits(number_string)

        # Assert
        self.assertEqual(result, expected_result)
