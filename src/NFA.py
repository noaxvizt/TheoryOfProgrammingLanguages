from src.State import State
import networkx as nx
import matplotlib.pyplot as plt


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
    self.enumerated_states - словарь, где ключ, это уникальный идентификатор состояния,
    а значение само состояние
    self.num_of_states - число состояний
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
        self.enumerated_states = dict()
        self.calculate_enumerate_states()
        self.num_of_states = 0
        self.update_num_of_states()

    def concatenate(self, other):
        """
        Конкатенирует к данному автомату другой
        результат остается в том, из которого мы вызвали функцию
        другой автомат будет удален после завершения исполнения функции
        :param other: принадлежит классу NFA
        """
        self.letters.update(other.letters)
        self.letters.add('eps')
        for key, value in other.data.items():
            self.data[key] = value  # добавляем все состояния из другого в исходный
        if self.finish_state not in self.data:
            self.data[self.finish_state] = dict()
        if 'eps' not in self.data[self.finish_state]:
            self.data[self.finish_state]['eps'] = []
        self.data[self.finish_state]['eps'].append(other.start_state)
        self.finish_state.cancel_token()
        self.finish_state = other.finish_state
        self.calculate_enumerate_states()
        self.update_num_of_states()

    def add(self, other):
        """
        Прибавляет к данному автомату другой
        результат остается в том, из которого мы вызвали функцию
        другой автомат будет удален после завершения исполнения функции
        :param other: принадлежит классу NFA
        """
        self.letters.update(other.letters)
        self.letters.add('eps')
        new_start_state = State(None)
        new_finish_state = State(None)
        for key, value in other.data.items():
            self.data[key] = value
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
        self.calculate_enumerate_states()
        self.update_num_of_states()

    def iterate(self):
        """
        Делает итерацию автомата
        результат остается в исходном автомате
        """
        self.letters.add('eps')
        new_start_state = State(None)
        new_finish_state = State(None)
        self.data[new_start_state] = dict()
        self.data[new_start_state]['eps'] = []
        self.data[new_start_state]['eps'].append(self.start_state)
        self.data[new_start_state]['eps'].append(new_finish_state)
        if self.finish_state not in self.data:
            self.data[self.finish_state] = dict()
        if 'eps' not in self.data[self.finish_state]:
            self.data[self.finish_state]['eps'] = []
        self.data[self.finish_state]['eps'].append(new_finish_state)
        self.data[self.finish_state]['eps'].append(self.start_state)
        self.start_state = new_start_state
        self.finish_state.cancel_token()
        self.finish_state = new_finish_state
        self.calculate_enumerate_states()
        self.update_num_of_states()

    def visualise(self, print_start_finish_state=True):
        """
        Выводит графическое представление графа
        """
        if print_start_finish_state:
            print(f'Стартовая вершина с номером {self.start_state.counter}'
                  f'\nКонечная вершина с номером {self.finish_state.counter}')
        self.NFAGraph = nx.DiGraph(directed=True)
        self.edges = dict()
        for state in self.data:
            for letter in self.data[state]:
                for state1 in self.data[state][letter]:
                    self.edges[(str(hash(state)), str(hash(state1)))] = letter
        self.NFAGraph.add_edges_from(list(self.edges.keys()))
        pos = nx.kamada_kawai_layout(self.NFAGraph)
        nx.draw(self.NFAGraph, pos, with_labels=True)
        nx.draw_networkx_edge_labels(self.NFAGraph, pos, edge_labels=self.edges)
        plt.show()

    def calculate_enumerate_states(self):
        """
        Функция считает словарь self.enumerated_states, где ключ -
        уникальный индекс состояния, а значение само состояние
        """
        for state1 in self.data.keys():
            if state1.counter not in self.enumerated_states:
                self.enumerated_states[state1.counter] = state1
            for letter1 in self.data[state1]:
                for state2 in self.data[state1][letter1]:
                    if state2.counter not in self.enumerated_states:
                        self.enumerated_states[state2.counter] = state2

    def update_num_of_states(self):
        self.num_of_states = len(self.enumerated_states.keys())

    def eps_closure(self, states):
        """
        Функция возвращает множество вершин, доступных по e-переходам из исходного множества
        Множество вершин задается числом, бинарная запись которого содержит 1
        тогда и только тогда когда вершина с этим номером дежит во множестве
        :param states: целое число - исходное множетство состояний
        :return: возвращается целое число
        """
        available_states = states
        for iteration in range(self.num_of_states):
            for state in self.enumerated_states.keys():
                if (1 << state) & available_states:
                    if self.enumerated_states[state] in self.data and 'eps' in self.data[self.enumerated_states[state]]:
                        for neighbour_state in self.data[self.enumerated_states[state]]['eps']:
                            available_states |= 1 << neighbour_state.counter
        return available_states

    def letter_transition(self, states, letter):
        """
        Функция возвращает множество вершин, доступных по переходу из множества states
        по букве letter
        :param states: целое число - исходное множество состояний
        :param letter буква, по которой осуществляется переход
        :return: возвращается целое число, множество вершин, которые доступны по букве letter
        из множества состояний state
        """
        available_states = 0
        for state in self.enumerated_states.keys():
            if (1 << state) & states:
                if self.enumerated_states[state] in self.data and letter in self.data[self.enumerated_states[state]]:
                    for neighbour_state in self.data[self.enumerated_states[state]][letter]:
                        available_states |= 1 << neighbour_state.counter
        return available_states




