from src.State import State
from src.NFA import NFA
from src.Node import Node
from src.RegularExpression import RegularExpression
from src.grammar_check import grammar_check
from src.make_parsing_tree import make_parsing_tree
from src.make_NFA_from_parsing_tree import make_NFA_from_parsing_tree
from src.DFS_in_parsing_tree import DFS

reg = RegularExpression(input())
start_node = make_parsing_tree(reg.expression)
NFA = make_NFA_from_parsing_tree(start_node)
NFA.visualise()









