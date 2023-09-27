'''
basparser

Analizador Lexico para el lenguaje BASIC Darmounth 64
'''
import logging
import sly
from baslex import Lexer


class Parser(sly.Parser):
    log = logging.getLogger()
    log.setLevel(logging.ERROR)
    expected_shift_reduce = 1
    debugfile = 'basic.txt'

    tokens = Lexer.tokens

    # Implementacion Reglas de la Gramatica

    @_("program statement")
    def program(self, p):
        ...

    @_("statement")
    def program(self, p):
        ...

    @_("error")
    def program(self, p):
        ...

    @_("INTEGER command NEWLINE")
    def statement(self, p):
        ...

    @_("INTEGER NEWLINE")
    def statement(self, p):
        ...

    @_("INTEGER error NEWLINE")
    def statement(self, p):
        ...

    @_("NEWLINE")
    def statement(self, p):
        ...

    # LET statement

    @_("LET variable '=' expr")
    def command(self, p):
        ...

    @_("LET variable '=' error")
    def command(self, p):
        ...

    # READ statement

    @_("READ varlist")
    def command(self, p):
        ...

    @_("READ error")
    def command(self, p):
        ...

    # DATA statement

    @_("DATA numlist")
    def command(self, p):
        ...

    @_("DATA error")
    def command(self, p):
        ...

    # PRINT statement

    @_("PRINT plist optend")
    def command(self, p):
        ...

    @_("PRINT error")
    def command(self, p):
        ...

    @_("PRINT")
    def command(self, p):
        ...

    # GOTO statement

    @_("GOTO INTEGER")
    def command(self, p):
        ...

    @_("GOTO error")
    def command(self, p):
        ...

    # IF-THEN statement

    @_("IF relexpr THEN INTEGER")
    def command(self, p):
        ...

    @_("IF error THEN INTEGER")
    def command(self, p):
        ...

    @_("IF relexpr THEN error")
    def command(self, p):
        ...

    # FOR statement

    @_("FOR ID '=' expr TO expr optstep")
    def command(self, p):
        ...

    @_("FOR ID '=' error TO expr optstep")
    def command(self, p):
        ...

    @_("FOR ID '=' expr TO error optstep")
    def command(self, p):
        ...

    @_("FOR ID '=' expr TO expr STEP error")
    def command(self, p):
        ...

    # NEXT statement

    @_("NEXT ID")
    def command(self, p):
        ...

    @_("NEXT error")
    def command(self, p):
        ...

    # END statement

    @_("END")
    def command(self, p):
        ...

    # REM statement

    @_("REM")
    def command(self, p):
        ...

    # STOP statement

    @_("STOP")
    def command(self, p):
        ...

    # DEF statement

    @_("DEF ID '(' ID ')' '=' expr")
    def command(self, p):
        ...

    @_("DEF ID '(' ID ')' '=' error")
    def command(self, p):
        ...

    @_("DEF ID '(' error ')' '=' expr")
    def command(self, p):
        ...

    # GOSUB statement

    @_("GOSUB INTEGER")
    def command(self, p):
        ...

    @_("GOSUB error")
    def command(self, p):
        ...

    # RETURN statement

    @_("RETURN")
    def command(self, p):
        ...

    # DIM statement

    @_("DIM dimlist")
    def command(self, p):
        ...

    @_("DIM error")
    def command(self, p):
        ...

    # Lista de variables proporcionadas DIM statement

    @_("dimlist ',' dimitem")
    def dimlist(self, p):
        ...

    @_("dimitem")
    def dimlist(self, p):
        ...

    # DIM items

    @_("ID '(' INTEGER ')'")
    def dimitem(self, p):
        ...

    @_("ID '(' INTEGER ',' INTEGER ')'")
    def dimitem(self, p):
        ...

    # Expresiones Aritmeticas

    @_("expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr",
       "expr '^' expr")
    def expr(self, p):
        ...

    @_("INTEGER", "FLOAT")
    def expr(self, p):
        ...

    @_("variable")
    def expr(self, p):
        ...

    @_("'(' expr ')'")
    def expr(self, p):
        ...

    @_("'-' expr")
    def expr(self, p):
        ...

    # Expresiones de Relacion

    @_("expr LT expr",
       "expr LE expr",
       "expr GT expr",
       "expr GE expr",
       "expr '=' expr",
       "expr NE expr")
    def relexpr(self, p):
        ...

    # Variables

    @_("ID")
    def variable(self, p):
        ...

    @_("ID '(' expr ')'")
    def variable(self, p):
        ...

    @_("ID '(' expr ',' expr ')'")
    def variable(self, p):
        ...

    # Reglas opcionales

    @_("','", "';'", "empty")
    def optend(self, p):
        ...
    
    @_("STEP expr", "empty")
    def optstep(self, p):
        ...

    @_("varlist ',' variable")
    def varlist(self, p):
        ...

    @_("variable")
    def varlist(self, p):
        ...

    @_("numlist ',' number")
    def numlist(self, p):
        ...

    @_("number")
    def numlist(self, p):
        ...

    # Numeros

    @_("INTEGER", 'FLOAT')
    def number(self, p):
        value:float

    @_("'-' INTEGER", "'-' FLOAT")
    def number(self, p):
        value: int

    # lista de cosas a imprimir

    @_("plist ',' pitem")
    def plist(self, p):
        ...

    @_("pitem")
    def plist(self, p):
        ...

    @_("STRING")
    def pitem(self, p):
        value: str

    @_("STRING expr")
    def pitem(self, p):
        ...

    @_("expr")
    def pitem(self, p):
        ...

    @_("")
    def empty(self, p):
        ...

    def error(self, p):
        ...

if __name__ == '__main__':
    p = Parser()