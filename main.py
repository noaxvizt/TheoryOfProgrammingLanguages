from src.Scanner import Scanner
import sys

# Пример
"""tokens = [['STR', 'str'],
          ['INT', 'int'],
          ['SEMICOLON', ';'],
          ['EQUAL', '='],
          ['VAR', 'var(0+1)*'],
          ['STRING', '"(a+b+c)*"'],
          ['NUM', '0+1(0+1)*']]
string = 'str var001 = "babac" ;'
scanner = Scanner(tokens)
print(scanner.parse_string(string))"""

print("Введите токены и регулярные выражения через пробел по одной паре в строчку."
      "После того как вы ввесли все токены введите пустую строку")
tokens = []
while True:
    now_input = input()
    if len(now_input) == 0:
        break
    tokens.append(now_input.split(' '))
print("Введите строку, которую нужно распарсить")
string = input()
scanner = Scanner(tokens)
parsed_string = scanner.parse_string(string)
print(parsed_string)

"""
input:

STR str
INT int
SEMICOLON ;
EQUAL =
VAR var(0+1)*
STRING "(a+b+c)*"
NUM 0+1(0+1)*
    
str var001 = "babac" ;

"""