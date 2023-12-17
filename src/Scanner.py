from src.reg_to_NFA import regex_to_nfa
from src.RegularExpression import RegularExpression
from src.State import State
from src.parse_tokens_to_NFA import parse_tokens_to_NFA
from src.union_NFA import union_NFA
from src.DFA import DFA


tokens = [['STR', 'str'],
          ['INT', 'int'],
          ['SEMICOLON', ';'],
          ['EQUAL', '='],
          ['VAR', 'var(0+1)*'],
          ['STRING', '"(a+b+c)*"'],
          ['NUM', '0+1(0+1)*']]
"""
tokens = [['VAR', 'var(0+1)*'],
          ['NUM', '0+1(0+1)*']]
"""

tokens_NFA, finish_states_NFA = parse_tokens_to_NFA(tokens)
print(finish_states_NFA)
main_NFA = union_NFA(tokens_NFA)
main_DFA = DFA(main_NFA)
main_DFA.visualise()
# main_NFA.visualise(print_start_finish_state=True)
# print(main_NFA.start_state.counter)



