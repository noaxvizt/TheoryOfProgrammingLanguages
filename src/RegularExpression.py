from src.grammar_check import grammar_check


class RegularExpression:
    """
    Класс для хранения регулярного выражения
    """
    def __init__(self, expression):
        """
        :param expression: String
        """
        if grammar_check(expression):
            self.expression = expression
        else:
            self.expression = ''
