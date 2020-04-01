class StringCalculator:
    def add(self, numbers):
        numbers_list = filter(bool, self.__unify_expression(numbers).split(','))
        numbers_list = list(map(int, numbers_list))

        negative_numbers = [x for x in numbers_list if x < 0]

        if negative_numbers:
            raise ValueError(f"Negatives not allowed: {','.join(map(str, negative_numbers))}")

        return sum([x for x in numbers_list if x < 1001])

    def __get_delimiters(self, str):
        if str[0:3] == '//[':
            first_line = str.split('\n', 1)[0]
            delimiters = first_line[3:-1].split('][')
        elif str[0:2] == '//':
            delimiters = str[2]
        else:
            delimiters = [',']

        return delimiters

    def __unify_expression(self, str):
        if str[:2] == '//':
            exp = str.split('\n', 1)[1]
        else:
            exp = str

        for delimiter in self.__get_delimiters(str):
            exp = exp.replace(delimiter, ',').replace('\n', ',')

        return exp
