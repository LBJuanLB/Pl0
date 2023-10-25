from plex import *
from pparse import *

from rich import print
with open("test2/assign1.pl0","r") as archivo:
    code = archivo.read()

lex = Lexer()
pas = Parser()
for tok in lex.tokenize(code):
  print(tok)

ast = pas.parse(lex.tokenize(code))
print(ast)