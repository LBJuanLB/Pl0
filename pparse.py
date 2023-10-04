'''
basparser

Analizador Lexico para el lenguaje BASIC Darmounth 64
'''
import logging
import sly
from plex import Lexer


class Parser(sly.Parser):
    log = logging.getLogger()
    log.setLevel(logging.ERROR)
    expected_shift_reduce = 1
    debugfile = 'basic.txt'

    tokens = Lexer.tokens

    # Implementacion Reglas de la Gramatica

    @_('function')
    def program(self, p):
        return p.function

    @_('FUN name "(" arguments ")" locals BEGIN statements END')
    def function(self, p):
        
        print("Definición de función:", p.name)
        print("Argumentos:", p.arguments)
        print("Locales:", p.locals)
        print("Declaraciones:", p.statements)
        return p
    
   
    @_("statement (';' statement)*")
    def statements(self, p):
        return [p.statement] + p.statements
    
    @_("'WHILE' relation 'do' statement")
    def statement(self, p):
        ...
    @_("'if' relation 'then' statement 'else' statement")
    def statement(self, p):
        ...

    @_("location ':''=' expr")
    def statement(self, p):
        ...
    @_("'print''('literal')'")
    def statement(self, p):
        ...
    @_("'write''('expr')'")
    def statement(self, p):
        ...
    @_("'read''('location')'")
    def statement(self, p):
        ...
    @_("'return' expr")
    def statement(self, p):
        ...
        
    @_("name'('exprlist')'")
    def statement(self, p):
        ...
    @_("'skip'")
    def statement(self, p):
        ...
    @_("'break'")
    def statement(self, p):
        ...
    @_("'begin' statements 'end'")
    def statement(self, p):
        ...
        
   
    @_("expr '+' expr")
    def expr(self, p):
        # Suma: expr + expr
        if len(p) == 3 and p[1] == '+':
            result = p[0] + p[2]
        return result
    @_("expr '-' expr")
    def expr(self, p):
        # Resta: expr - expr
        if len(p) == 3 and p[1] == '-':
            result = p[0] - p[2]
        return result
    @_("expr '*' expr")
    def expr(self, p):
        #Multiplicación: expr * expr
        if len(p) == 3 and p[1] == '*':
            result = p[0] * p[2]
        return result
    @_("expr '/' expr")
    def expr(self, p):
        # División: expr / expr
        if len(p) == 3 and p[1] == '/':
            result = p[0] / p[2]
        return result
    @_( "'-' expr")
    def expr(self, p):
        # Operador unario '-' (negación)
        if p[0] == '-':
            result = -p[1]
        return result
    @_( "'+' expr")
    def expr(self, p):
        # Operador unario '-' (negación)
        if p[0] == '+':
            result = p[1]
        return result
    @_( "'(' expr ')'")
    def expr(self, p):
        # Paréntesis: '(' expr ')'
        if p[0] == '(' and p[2] == ')':
            result = p[1]
        return result
    @_( "name '(' exprlist ')'")
    def expr(self, p):
        ...
      
    @_( "name")
    def expr(self, p):
       # Variable name
        if isinstance(p[0], str):
            result = p[0]
        return result
    @_( "name '[' INT ']'")
    def expr(self, p):
        # Variable con índice: name '[' INT ']'
         if len(p) == 4 and p[1] == '[' and isinstance(p[2], int) and p[3] == ']':
            ...
    @_( "num")
    def expr(self, p):
        # Número entero o flotante
        if isinstance(p[0], (int, float)):
            result = p[0]
        return result
    @_( "'INT' '(' expr ')'","'FLOAT' '(' expr ')'")
    def expr(self, p):
        # Casting a INT o FLOAT: ('INT' | 'FLOAT') '(' expr ')'
        if len(p) == 4 and p[0] in ['INT', 'FLOAT',"int","float"] and p[1] == '(' and p[3] == ')':
            if p[0] == 'INT':
                result = int(p[2])
            elif p[0] == 'FLOAT':
                result = float(p[2])
            elif p[0] == 'int':
                result = int(p[2])
            elif p[0] == 'float':
                result = float(p[2])
        return result
    



    @_("expr (',' expr)+")
    def exprlist(self, p):
        ...
    
    @_("relation 'and' relation","relation 'or' relation")
    def  relation(self, p):
        ...
    @_("'NOT' relation ")
    def  relation(self, p):
        ...
    @_("'(' relation ')'")
    def  relation(self, p):
        ...
    @_("expr '>' expr")
    def  relation(self, p):
        ...
    @_("expr '<' expr")
    def  relation(self, p):
        ...
    @_(" expr '>''=' expr")
    def  relation(self, p):
        ...
    @_("expr '<''=' expr")
    def  relation(self, p):
        ...
    @_("expr '=''=' expr")
    def  relation(self, p):
        ...
    @_("expr '!''=' expr")
    def  relation(self, p):
        ...
      
    @_("name ':' 'INT' ")
    def  arg(self, p):
        ...
    @_("name ':' 'FLOAT' ")
    def  arg(self, p):
        ...
    @_("name ':'  'INT' '[' int ']'")
    def  arg(self, p):
        ...
        
    @_("arg (',' arg)*")
    def  arglist(self, p):
        ...
    
    @_("(arg ';' | function ';')*")
    def locals(self, p):
        ...
    
    @_("name ")
    def location(self, p):
        ...
    @_("name '[' int ']'")
    def location(self, p):
        ...
    
    @_("int")
    def num(self, p):
        ...
    @_("float")
    def num(self, p):
        ...
    
    @_("((\+|-)?[1-9][0-9]*)|[0]")
    def int(self, p):
        return [p.statement] + p.statements

    @_("(\+|-)?([0]|[1-9][0-9]*)(\.[0-9]+((e|E)(\+|-)?[0-9]+)?")
    def FLOAT(self,p):
        return p
    @_("(e|E)(\+|-)?[0-9]+)")
    def FLOAT(self,p):
        return p
    
    @_("'INT' '[' int ']'") 
    def array(self, p):
        ...
    @_("'FLOAT' '[' float ']'") 
    def array(self, p):
        ...
        
    @_("[a-zA-Z_]+[0-9-a-zA-Z_]*") 
    def name(self, p):
        ...
        
    @_(".*")
    def  literal(self, p):
        ...
   

    
 

if __name__ == '__main__':
    p = Parser()
    lex=Lexer()
    p.parse(lex.tokenize)