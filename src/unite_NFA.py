def unite_NFA(tokens_NFA):
    """
    Функция, которая объединяет НКА распознающая токены в один
    :param tokens_NFA: список НКА, распознающих токены
    :return: NFA - НКА, распознающий все токены
    """
    for index in range(1, len(tokens_NFA)):
        tokens_NFA[0].add(tokens_NFA[index])
    return tokens_NFA[0]
