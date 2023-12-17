from src.State import State
from src.reg_to_NFA import regex_to_nfa
from src.RegularExpression import RegularExpression


def parse_tokens_to_NFA(tokens):
    """
    Функция из списка списков типа имя токена, регулярное значения,
    создает для каждого токена НКА, распознающий его
    :param tokens: list
    :return: tokens_NFA, finish_states_NFA
    tokens_NFA - список NFA, распознающих токены
    finish_states_NFA - список уникальных идентификаторов завершающих состояний
    для НКА, в котором записано имя токена
    """
    tokens_NFA = []
    finish_states_NFA = []
    ERROR_STATE = State('ERROR')
    finish_states_NFA.append((ERROR_STATE.counter, ERROR_STATE.token_name))
    for (token, regex) in tokens:
        current_nfa = regex_to_nfa((RegularExpression(regex)))
        current_nfa.finish_state.assign_token(token)
        if current_nfa.finish_state not in current_nfa.data:
            current_nfa.data[current_nfa.finish_state] = dict()
        if ' ' not in current_nfa.data[current_nfa.finish_state]:
            current_nfa.data[current_nfa.finish_state][' '] = []
        current_nfa.data[current_nfa.finish_state][' '].append(ERROR_STATE)
        current_nfa.letters.add(' ')
        finish_states_NFA.append((current_nfa.finish_state.counter, current_nfa.finish_state.token_name))
        current_nfa.finish_state = ERROR_STATE
        tokens_NFA.append(current_nfa)
    return tokens_NFA, finish_states_NFA
