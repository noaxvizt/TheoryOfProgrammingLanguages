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