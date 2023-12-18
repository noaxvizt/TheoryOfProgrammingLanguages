def grammar_check(expression):
    """
    :param expression: String
    :return: Bool - корректность регулярного выражения
    Регулярное выражение имеет вид
    a - буква
    AB - конкатенация регулярных выражений
    A+B - объединение регулярных выражений
    (A) - выделение регулярного выражения в скобки
    (A)* - итерация регулярного выражения
    говоря про регулярные выражения, подразумеваем,
    что работаем с регулярынми языками, задаваемыми данными регулярными выражениями
    То есть не должно быть ++, выражение не должно начинаться на + и окначиваться им,
    все * должны идти только после ),
    скобочный итог не должен быть отрицательным ни на каком шаге и в конце должен равняться нулю,
    и все заключенные в скобки регулярные выражения также должны быть корректными регулярными выражениями
    """

    """
    проверка корректности расстановки скобок
    """
    bracket_total = 0
    for symbol in expression:
        if symbol == '(':
            bracket_total += 1
        elif symbol == ')':
            bracket_total -= 1
            if bracket_total < 0:
                raise SyntaxError
    if bracket_total != 0:
        raise SyntaxError

    """
    проверка итерации
    """
    for index in range(len(expression)):
        if expression[index] == '*':
            if index == 0 or expression[index - 1] != ')':
                raise SyntaxError

    """
    проверка на корректность знака объединения
    """
    if '++' in expression or expression[0] == '+' or expression[-1] == '+':
        raise SyntaxError

    """
    проверка на корректность всех выражений в скобках
    """
    bracket_total = 0
    expression_in_brackets = ''
    for symbol in expression:
        if symbol == '(':
            bracket_total += 1
        if bracket_total > 0:
            expression_in_brackets += symbol
        if symbol == ')':
            bracket_total -= 1
            if bracket_total == 0:
                try:
                    grammar_check(expression_in_brackets[1: -1])
                except SyntaxError:
                    raise SyntaxError
            expression_in_brackets = ''
