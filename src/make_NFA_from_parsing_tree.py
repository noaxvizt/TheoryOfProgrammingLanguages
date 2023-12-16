from src.NFA import NFA


def make_NFA_from_parsing_tree(node):
    """
    Функция создает НКА из дерева разбора
    :param node: Node - корневая вершина дерева Разбора
    :return: NFA - недетерминированный конечный автомат
    """
    if node.type == 's':
        return NFA(node.value)
    elif node.type == 'u':
        node_left_NFA = make_NFA_from_parsing_tree(node.left)
        node_left_NFA.iterate()
        return node_left_NFA
    elif node.type == 'b':
        if node.value == '+':
            node_left_NFA = make_NFA_from_parsing_tree(node.left)
            node_right_NFA = make_NFA_from_parsing_tree(node.right)
            node_left_NFA.add(node_right_NFA)
            return node_left_NFA
        elif node.value == '&':
            node_left_NFA = make_NFA_from_parsing_tree(node.left)
            node_right_NFA = make_NFA_from_parsing_tree(node.right)
            node_left_NFA.concatenate(node_right_NFA)
            return node_left_NFA
