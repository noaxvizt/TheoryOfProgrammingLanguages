from collections import deque
"""

"""


class Scanner:
    def __init__(self, DFA, vertexes, letters, start_vertex, receiving_vertexes, error_vertexes, tokens):
        self.DFA = DFA
        self.vertexes = vertexes
        self.letters = letters
        self.start_vertex = start_vertex
        self.receiving_vertexes = receiving_vertexes
        self.error_vertexes = error_vertexes
        self.tokens = tokens

    def scan(self, line):
        index = 0
        stack = deque()
        answer = []
        now_state = self.start_vertex
        stack.append((now_state, index))
        while index < len(line):
            now_letter = line[index]
            now_state = self.DFA[now_state][now_letter]
            if now_state in self.error_vertexes:
                while len(stack) and stack[-1][0] not in self.receiving_vertexes:
                    stack.pop()
                if len(stack) == 0:
                    raise SyntaxError
                index = stack[-1][1]
                answer.append((self.tokens[stack[-1][0]], line[stack[0][1]: stack[-1][1]]))
                stack.clear()
                now_state = self.start_vertex
            stack.append((now_state, index))
            index += 1

        while len(stack) and stack[-1][0] not in self.receiving_vertexes:
            stack.pop()
        if len(stack) == 0:
            pass
        else:
            index = stack[-1][1]
            answer.append((self.tokens[stack[-1][0]], line[stack[0][1]: stack[-1][1]]))
        stack.clear()
        return answer
