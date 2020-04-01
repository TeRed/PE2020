import re


class BitCounter:
    def no_of_bits(self, numbers):

        numbers = filter(None, re.split('\s|;', numbers))

        results = map(self.__no_of_bits_for_number, numbers)
        return sum(results)

    def __no_of_bits_for_number(self, number):
        base = 10
        if number.startswith('$'):
            base = 16
            number = number[1:]

        try:
            number = int(number, base)
        except Exception:
            raise Exception('String contains illegal characters.')

        if number < 0 or number > 255:
            raise Exception('Number out of range.')

        number_bit_string = '{0:b}'.format(number)
        positives = [i for i in list(number_bit_string) if i == '1']

        return len(positives)
