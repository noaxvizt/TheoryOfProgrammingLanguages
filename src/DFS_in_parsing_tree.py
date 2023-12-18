def DFS(node):
    """
    Функция для отладки. Совершает обход по дереву разбора регулярного выражения
    :param node: Корень дерева
    :return:
    """
    print(node.value)
    if node.type == 'u':
        DFS(node.left)
    if node.type == 'b':
        DFS(node.left)
        DFS(node.right)
