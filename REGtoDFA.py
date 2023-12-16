"""
пример токенов с их возможными лексемами
имя токена  -   пример      регулярное выражение
STR         -   str         str
INT         -   int         int
SEMICOLON   -   ;           ;
EQUAL       -   =           =
VAR         -   var1001     var(0+1)*
STRING      -   "abacab"    "(a+b+c)*"
NUM         -   101         0+1(0+1)*


можем получить на вход строку
str var001 = "babac" ;


итого на вход должны получить следующее
Имя токена  регулярное выражение
STR str
INT int
SEMICOLON ;
EQUAL =
VAR var(0+1)*
STRING "(a+b+c)*"
NUM 0+1(0+1)*

после каждой лексеммы ожидается пробел, кроме ;
Даже после предпоследней лексемы перед ; ожидается пробел

В регулярном выражении могут быть только строчные буквы латинского алфавита, цифры,
скобки, расстановка которых является правильной
Каждому НКА соотвествует регулярное выражение
Мы будет говорит, что конкатенируем НКА A и B, если в в результате исполнения функции
получим автомат, который распознает регулярный язык, являющийся конкатенацией регулярных
языков, распознаваемых НКА A и B
Анологично с сложением, и итерацией
"""


class State:
    """
    класс состояния автомата
    содержит в себе информацию о принимаемости self.receiving
    содердит в себе токен состояния или None в случае непринимаемости
    """

    def __init__(self, token_name=None):
        """
        :param token_name: название токена, если состояяние принимающее
        """
        if token_name is not None:
            self.receiving = True
            self.token_name = token_name
        else:
            self.receiving = False

    def get_token(self):
        """
        :return: Возвращает имя токена
        """
        return self.token_name

    def assign_token(self, token_name):
        """
        :param token_name: название токена
        делает состояние принимающим, именует токен
        """
        self.receiving = True
        self.token_name = token_name

    def cancel_token(self):
        """
        делает состояние непринимающим
        """
        self.receiving = False
        self.token_name = None


class NFA:
    """
    Класс недетерминированного конечного автомата
    содержит в себе:
    self.letters - множество используемых букв
    self.start_state - стартовое состояние
    self.finish_state - конечное состояние
    self.data - словарь
    пример: self.data[state_from][letter] = state_to
    self.data[state_from] - словарь
    self.data[state_from][letter] - список
    state_from state_to соответственно состояния
    letter - буква, по которой осуществляется переход
    НКА содержит одно стартовое и одно конечное состояние
    """

    def __init__(self, letter='eps'):
        """
        Создает НКА, у которого переход от стартовой к конечной вершине по букве letter
        :param letter: буква (по умолчанию пустая строка)
        """
        self.letters = set()
        self.letters.add(letter)
        self.start_state = State(None)
        self.finish_state = State(None)
        self.data = dict()
        self.data[self.start_state] = dict()
        self.data[self.start_state][letter] = []
        self.data[self.start_state][letter].append(self.finish_state)

    def concatenate(self, other):
        """
        Конкатенирует к данному автомату другой
        результат остается в том, из которого мы вызвали функцию
        другой автомат будет удален после завершения исполнения функции
        :param other: принадлежит классу NFA
        """
        self.letters.union(other.letters)
        self.letters.add('eps')
        for state in other.data:
            self.data[state] = other.data[state]  # добавляем все состояния из другого в исходный
        if self.finish_state not in self.data:
            self.data[self.finish_state] = dict()
        if 'eps' not in self.data[self.finish_state]:
            self.data[self.finish_state]['eps'] = []
        self.data[self.finish_state]['eps'].append(other.start_state)
        self.finish_state.cancel_token()
        self.finish_state = other.finish_state
        del other

    def add(self, other):
        """
        Прибавляет к данному автомату другой
        результат остается в том, из которого мы вызвали функцию
        другой автомат будет удален после завершения исполнения функции
        :param other: принадлежит классу NFA
        """
        self.letters.union(other.letter)
        self.letters.add('eps')
        new_start_state = State(None)
        new_finish_state = State(None)
        for key in other.data:
            self.data[key] = other.data[key]
        self.data[new_start_state] = dict()
        self.data[new_start_state]['eps'] = []
        self.data[new_start_state]['eps'].append(self.start_state)
        self.data[new_start_state]['eps'].append(other.start_state)
        if self.finish_state not in self.data:
            self.data[self.finish_state] = dict()
        if 'eps' not in self.data[self.finish_state]:
            self.data[self.finish_state]['eps'] = []
        self.data[self.finish_state]['eps'].append(new_finish_state)
        if other.finish_state not in self.data:
            self.data[other.finish_state] = dict()
        if 'eps' not in self.data[other.finish_state]:
            self.data[other.finish_state]['eps'] = []
        self.data[other.finish_state]['eps'].append(new_finish_state)
        self.start_state = new_start_state
        self.finish_state.cancel_token()
        other.finish_state.cancel_token()
        self.finish_state = new_finish_state

    def iteration(self):
        """
        Делает итерацию автомата
        результат остается в исходном автомате
        """
        self.letters.add('eps')
        new_start_state = State(None)
        new_finish_state = State(None)
        self.data[new_start_state]['eps'] = []
        self.data[new_start_state]['eps'].append(self.start_state)
        self.data[new_start_state]['eps'].append(new_finish_state)
        if self.finish_state not in self.data:
            self.data[self.finish_state] = dict()
        if 'eps' not in self.data[self.finish_state]:
            self.data[self.finish_state]['eps'] = []
        self.data[self.finish_state]['eps'].append(new_finish_state)
        self.data[self.finish_state]['eps'].appned(self.start_state)
        self.start_state = new_start_state
        self.finish_state.cancel_token()
        self.finish_state = new_finish_state


class Node:
    """
    Класс Нода - вершины из дерева разбора
    Может быть оператором и иметь потомков или быть символом и быть листом
    Оператор может иметь двух потомков в случае, когда оператор:
    + - объединение
    & - конкатенация
    Тогда Нода будет иметь тип 'b' - binary

    или одного потомка в случае, когда оператор:
    * - итерация
    Тогда Нода будет иметь тип 'u' - unary

    Символ не имеет потомков
    Тогда Нода будет иметь тип 's' - symbol
    """

    _counter = 0
    """
    переменная, считающая количество экзепляров класса
    """
    def __init__(self, value='&'):
        Node._counter += 1
        if value in ('+', '&'):
            self.type = 'b'
            self.left = None
            self.right = None
        elif value == '*':
            self.type = 'u'
            self.left = None
        else:
            self.type = 's'


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
    try:
        # проверка корректности расстановки скобок
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

        # проверка итерации
        for index in range(len(expression)):
            if expression[index] == '*':
                if index == 0 or expression[index - 1] != ')':
                    raise SyntaxError

        # проверка на корректность знака объединения
        if '++' in expression or expression[0] == '+' or expression[-1] == '+':
            raise SyntaxError

        # проверка на корректность всех выражений в скобках
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
    except SyntaxError:
        return False
    return True


def make_parsing_tree(regular_expression):
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

    expression = regular_expression.expression
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
            return Node
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













