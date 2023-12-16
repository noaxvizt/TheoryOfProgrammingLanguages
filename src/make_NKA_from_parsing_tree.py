from src.NFA import NFA


def make_NFA_from_parsing_tree(node):
    """
    Функция создает НКА из дерева разбора
    :param node: Node - корневая вершина дерева Разбора
    :return: NFA - недетерминированный конечный автомат
    """
    if node.type == 's':
        return NFA('a')
    elif node.type == 'u':
        return make_NFA_from_parsing_tree(node.left).iterate()
    elif node.type == 'b':
        if node.value == '+':
            return make_NFA_from_parsing_tree(node.left).add(make_NFA_from_parsing_tree(node.left))
        elif node.value == '&':
            return make_NFA_from_parsing_tree(node.left).concatenate(make_NFA_from_parsing_tree(node.left))