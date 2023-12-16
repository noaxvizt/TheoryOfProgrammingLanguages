from collections import deque
"""
введите нка в виде графа
на первой строчке n-количество вершин m-количество переходов
далее на следующих n строках принимается тройка в виде вершина1 вершина2 буква(е-переход обозначается как eps,
в остальных случаях ожидается одна буква латинского альфавита)
далее вводится стартовая
и на последней строчке вводятся принимающие вершины
"""

"""
ввод нка
"""
NFA_vertex_num, NFA_edges_num = map(int, input().split())
NFA = dict()
letters = set()
vertexes = set()
for i in range(NFA_edges_num):
    vertex1, vertex2, letter = input().split()
    vertexes.add(vertex1)
    vertexes.add(vertex2)
    if letter != 'eps':
        letters.add(letter)
    if vertex1 not in NFA:
        NFA[vertex1] = dict()
    if letter not in NFA[vertex1]:
        NFA[vertex1][letter] = []
    NFA[vertex1][letter].append(vertex2)
start_vertex = input()
receiving_vertexes = input().split()

"""
для того, чтобы хранить множества как двоичные числа
"""

vertex_list = list(vertexes)
numerate_vertex = dict()
for index, vertex in enumerate(vertex_list):
    numerate_vertex[vertex] = index

"""
функция для эпсилон замыкания
"""


def eps_closure(vertexes):
    available_vertexes = vertexes
    for iteration in range(NFA_vertex_num):
        for possible_vertex in range(NFA_vertex_num):
            if (1 << possible_vertex) & available_vertexes:
                if vertex_list[possible_vertex] in NFA and 'eps' in NFA[vertex_list[possible_vertex]]:
                    for neighb_vertexes in NFA[vertex_list[possible_vertex]]['eps']:
                        available_vertexes |= 1 << numerate_vertex[neighb_vertexes]
    return available_vertexes


"""
функция для получения множества вершин после перехода по букве
"""


def letter_trans(vertexes, letter):
    answer = 0
    for vertex in range(NFA_vertex_num):
        if (1 << vertex) & vertexes:
            if vertex_list[vertex] in NFA and letter in NFA[vertex_list[vertex]]:
                for neighbour_vertexes in NFA[vertex_list[vertex]][letter]:
                    answer |= 1 << numerate_vertex[neighbour_vertexes]
    return answer


"""
построение самого дка
"""

DFA = dict()
letters = list(letters)
queue = deque()
DFA_start_vertex = str(eps_closure(1 << numerate_vertex[start_vertex]))
queue.append(DFA_start_vertex)
while len(queue):
    now_vertex = queue.popleft()
    DFA[now_vertex] = dict()
    for letter in letters:
        neighbour_vertex = eps_closure(letter_trans(int(now_vertex), letter))
        DFA[now_vertex][letter] = neighbour_vertex
        if neighbour_vertex not in DFA:
            queue.append(neighbour_vertex)

DFA_receiving_vertexes = []
DFA_receiving_template = 0
for receiving_vertex in receiving_vertexes:
    DFA_receiving_template |= 1 << numerate_vertex[receiving_vertex]
for vertex in DFA.keys():
    if int(vertex) & DFA_receiving_template:
        DFA_receiving_vertexes.append(vertex)

DFA_vertex_list = DFA.keys()
DFA_numerate_vertex = dict()
for index, vertex in enumerate(DFA_vertex_list):
    DFA_numerate_vertex[vertex] = index

print("Количество вершин в ДКА", len(DFA_vertex_list))
print("Переходы")
for vertex in DFA:
    for letter in DFA[vertex]:
        print(DFA_numerate_vertex[vertex], DFA_numerate_vertex[DFA[vertex][letter]], letter)
print("Стартовая вершина", DFA_numerate_vertex[DFA_start_vertex])
print("Принимающие состояния", *[DFA_numerate_vertex[i] for i in DFA_receiving_vertexes])


"""
example
4 4
1 2 0
1 3 1
2 4 eps
3 4 eps
1
4
      (2)
     /   \
    0     eps
   /       \
(1)        (4) 
   \       /
    1    eps
     \  /
     (3)
"""




