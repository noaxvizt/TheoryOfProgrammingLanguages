from src.Scanner import Scanner
import sys


tokens = [['STR', 'str'],
          ['INT', 'int'],
          ['SEMICOLON', ';'],
          ['EQUAL', '='],
          ['VAR', 'var(0+1)*'],
          ['STRING', '"(a+b+c)*"'],
          ['NUM', '0+1(0+1)*']]
string = 'str var001 = "babac" ;'
scanner = Scanner(tokens)
print(scanner.parse_string(string))

