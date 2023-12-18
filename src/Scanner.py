from src.move_regular_expression_to_NFA import move_regular_expression_to_NFA
from collections import deque
from src.RegularExpression import RegularExpression
from src.State import State
from src.parse_tokens_to_NFA import parse_tokens_to_NFA
from src.unite_NFA import unite_NFA
from src.DFA import DFA

"""
tokens = [['STR', 'str'],
          ['INT', 'int'],
          ['SEMICOLON', ';'],
          ['EQUAL', '='],
          ['VAR', 'var(0+1)*'],
          ['STRING', '"(a+b+c)*"'],
          ['NUM', '0+1(0+1)*']]
"""
"""
tokens = [['VAR', 'var(0+1)*'],
          ['NUM', '0+1(0+1)*']]
"""


class Scanner:
    def __init__(self, tokens):
        tokens_NFA, finish_states_NFA = parse_tokens_to_NFA(tokens)
        main_NFA = unite_NFA(tokens_NFA)
        self.main_DFA = DFA(main_NFA)
        self.main_DFA.assign_tokens(finish_states_NFA)
        # self.main_DFA.visualise()

    def check_string(self, string):
        for letter in string:
            if letter not in self.main_DFA.letters:
                return False
        return True

    def parse_string(self, string):
        if not(self.check_string(string)):
            raise SyntaxError
        parsed_string = []
        states_sequence = deque()
        current_index = 0
        current_state = self.main_DFA.start_state
        while current_index != len(string):
            current_state = self.main_DFA.data[current_state][string[current_index]]
            if current_state.get_token() == 'ERROR':
                while len(states_sequence) != 0 and states_sequence[-1][1].get_token() is None:
                    states_sequence.pop()
                if len(states_sequence) != 0:
                    current_index = states_sequence[-1][0] + 1
                    current_state = self.main_DFA.start_state
                    parsed_string.append((string[states_sequence[0][0]: states_sequence[-1][0] + 1], states_sequence[-1][1].get_token()))
                    states_sequence.clear()
            else:
                states_sequence.append((current_index, current_state))
            current_index += 1
        while len(states_sequence) != 0 and states_sequence[-1][1].get_token() is None:
            states_sequence.pop()
        if len(states_sequence) != 0:
            parsed_string.append(
                (string[states_sequence[0][0]: states_sequence[-1][0] + 1], states_sequence[-1][1].get_token()))
            states_sequence.clear()
        return parsed_string






