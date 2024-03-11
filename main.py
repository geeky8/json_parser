from scanner import Scanner, Token, TokenType
from parser import Parser

# json = '{"foo":"bar", "doo": "boo"}'
json = '{ "foo" : [1, 2, "three"] }'
scanner = Scanner(json)
tokens = scanner.scan()
parser = Parser(tokens)
res = parser.parse()
print(res)