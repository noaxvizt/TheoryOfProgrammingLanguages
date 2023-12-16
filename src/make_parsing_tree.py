from src.Node import Node
from src.RegularExpression import RegularExpression


def make_parsing_tree(expression):
    """
    Функция, которая из регулярного выражения собирает дерево разбора
    :param regular_expression: RegularExpression - регулярное выражение, принимаемое на вход
    :return: node: Node - корневая вершина дерева разбора регулярного выражения

    Регулярное выражение разбирается по возрастанию приоритеторв операции
    0)a - буква
    1)+ - объединение
    2)& - конкатенация
    3)() выделение в скобки или ()* - итерация
    """

    """
    0) Проверка на букву
    """
    if len(expression) == 1:
        return Node(expression)
    """
    1) Проверка на возможность разделения по объединению
    """
    bracket_total = 0
    for index in range(len(expression)):
        if expression[index] == '(':
            bracket_total += 1
        elif expression[index] == ')':
            bracket_total -= 1
        if expression[index] == '+' and bracket_total == 0:
            node = Node('+')
            node.left = make_parsing_tree(expression[:index])
            node.right = make_parsing_tree(expression[index + 1:])
            return node
    """
    2) Проверка на конкатенацию
    """
    # слева
    if expression[0] != '(':
        node = Node('&')
        node.left = make_parsing_tree(expression[0])
        node.right = make_parsing_tree(expression[1:])
        return node
    # справа
    if expression[-1] != ')' and expression[-1] != '*':
        node = Node('&')
        node.left = make_parsing_tree(expression[:-1])
        node.right = make_parsing_tree(expression[-1])
        return node
    """
    3) Проверка на выражение в скобках
    """
    if expression[0] == '(':
        if expression[-1] == ')':
            return make_parsing_tree(expression[1:-1])
        elif expression[-1] == '*' and expression[-2] == ')':
            node = Node('*')
            node.left = make_parsing_tree(expression[1:-2])
            return node
    """
    4) Остальное считаем пустой строкой
    """
    node = Node('')
    return node
