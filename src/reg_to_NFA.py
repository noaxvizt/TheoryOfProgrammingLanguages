from src.make_parsing_tree import make_parsing_tree
from src.make_NFA_from_parsing_tree import make_NFA_from_parsing_tree


def regex_to_nfa(regular_expression):
    """
    Функция строит и возвращает НКА по регулярному выражению
    :param regular_expression: RegularExpression - регулярное выражение
    :return: NFA - НКА, полученный из регулярного выражения
    """
    start_node = make_parsing_tree(regular_expression.expression)
    NFA_from_regex = make_NFA_from_parsing_tree(start_node)
    return NFA_from_regex









