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


from src.State import State
from src.NFA import NFA
from src.Node import Node
from src.RegularExpression import RegularExpression
from src.grammar_check import grammar_check
from src.make_parsing_tree import make_parsing_tree
from src.make_NKA_from_parsing_tree import make_NFA_from_parsing_tree













