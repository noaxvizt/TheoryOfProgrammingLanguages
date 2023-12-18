from src.State import State, DFAState
from src.NFA import NFA
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


class DFA:
    def __init__(self, main_NFA):
        """
        Создает ДКА из НКА по алгоритму томсона
        :param main_NFA: NFA
        """
        self.letters = main_NFA.letters
        self.letters.discard('eps')
        leak_data = dict()
        queue = deque()
        start_state = main_NFA.eps_closure(1 << main_NFA.start_state.counter)
        queue.append(start_state)
        while len(queue):
            now_state = queue.popleft()
            leak_data[now_state] = dict()
            for letter in self.letters:
                neighbour_state = main_NFA.eps_closure(main_NFA.letter_transition(now_state, letter))
                leak_data[now_state][letter] = neighbour_state
                if neighbour_state not in leak_data:
                    queue.append(neighbour_state)
        """
        На данном этапе leak_data содерржит числа как элементы, заменим их на соотвествующие состояния
        """
        self.states_value = dict()
        self.data = dict()
        for key in leak_data.keys():
            if key not in self.states_value:
                self.states_value[key] = DFAState(key)
            if self.states_value[key] not in self.data:
                self.data[self.states_value[key]] = dict()
            for letter in self.letters:
                if leak_data[key][letter] not in self.states_value:
                    self.states_value[leak_data[key][letter]] = DFAState(leak_data[key][letter])
                self.data[self.states_value[key]][letter] = self.states_value[leak_data[key][letter]]
        self.start_state = self.states_value[start_state]

    def assign_tokens(self, finish_states_NFA):
        """
        Функция добавляет информацию о токенах в состояния ДКА
        :param finish_states_NFA: list
        binary_finish_states_NFA - словарь, где ключ - идентификатор состояния в двоичной системе,
        токен - имя токена
        """
        binary_finish_states_NFA = dict()
        binary_finish_state = 0
        for index_state, token in finish_states_NFA:
            binary_finish_states_NFA[1 << index_state] = token
            binary_finish_state |= 1 << index_state
        for state in self.data.keys():
            if state.value & binary_finish_state:
                state.assign_token(binary_finish_states_NFA[state.value & binary_finish_state])

    def visualise(self):
        """
        Выводит графическое представление графа
        """
        print("Стартовая вершина", hash(self.start_state))
        for state in self.data:
            print(state.counter, state.token_name)
        self.NFAGraph = nx.DiGraph(directed=True)
        self.edges = dict()
        for state in self.data:
            for letter in self.data[state]:
                state1 = self.data[state][letter]
                self.edges[(str(hash(state)), str(hash(state1)))] = letter
        self.NFAGraph.add_edges_from(list(self.edges.keys()))
        pos = nx.circular_layout(self.NFAGraph)
        nx.draw(self.NFAGraph, pos, with_labels=True)
        nx.draw_networkx_edge_labels(self.NFAGraph, pos, edge_labels=self.edges)
        plt.show()
