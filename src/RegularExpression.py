from src.grammar_check import grammar_check


class RegularExpression:
    """
    Класс для хранения регулярного выражения
    """
    def __init__(self, expression):
        """
        :param expression: String
        """
        try:
            grammar_check(expression)
        except SyntaxError:
            self.expression = ''
        else:
            self.expression = expression