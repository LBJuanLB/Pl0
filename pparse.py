'''
basparser

Analizador Lexico para el lenguaje BASIC Darmounth 64
'''
import logging
import sly
from arbol import *
from plex import Lexer


class Parser(sly.Parser):
    log = logging.getLogger()
    log.setLevel(logging.ERROR)
    expected_shift_reduce = 1
    debugfile = 'pl0.txt'

    tokens = Lexer.tokens
    # Implementacion Reglas de la Gramatica

    @_("funclist")
    def program(self, p):
        return Program(p.funclist)
    
    @_("function { function }")
    def funclist(self, p):
        return [p.function0] + [p.function1]
    
    @_("FUN NAME '(' [ arglist ] ')' locals BEGIN statements END")
    def function(self, p):
        function_name = p.name
        arguments = p.arglist
        locals = p.locals
        statements = p.statements

        return Funtion(function_name, arguments, locals, statements)
    
    @_("statement { ';' statement }")
    def statements(self, p):
        return [p.statement0] + [p.statement1]
    
    @_("WHILE relation DO statement")
    def statement(self, p):
        return While(p.relation, p.statement)

    @_("IF relation THEN statement [ ELSE statement ]")
    def statement(self, p):
        return If(p.relation, p[3], p[5])

    @_("location ASIG expr")
    def statement(self, p):
        return Assign(p.location, p.expr)
    
    @_("PRINT '(' LITERAL ')'")
    def statement(self, p):
        return Print(p[2])
    
    @_("WRITE '(' expr ')'")
    def statement(self, p):
        return Write(p.expr)
    
    @_("READ '(' location ')'")
    def statement(self, p):
        return Read(p.location)
    
    @_("RETURN expr")
    def statement(self, p):
        return Return(p.expr)
        
    @_("NAME '(' exprlist ')'")
    def statement(self, p):
        return FunCall(p[0], p[2])

    @_("SKIP")
    def statement(self, p):
        return Skip()
    
    @_("BREAK")
    def statement(self, p):
        return Break()
    
    @_("BEGIN statements END")
    def statement(self, p):
        return Begin(p.statements)
   
    @_("expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr")
    def expr(self, p):
        return Binary(p[1], p[0], p[1])
    
    @_("'-' expr",
       "'+' expr")
    def expr(self, p):
        return Unary(p[0], p.expr)

    @_( "'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("NAME '[' expr ']'")
    def expr(self, p):
        return ArrayLocation(p[0], p[2])

    @_("NAME '(' exprlist ')'")
    def expr(self, p):
        return FunCall(p[0], p[2])

    @_("NAME")
    def expr(self, p):
        return SimpleLocation(p[0])

    @_("INT",
       "FLOAT")
    def expr(self, p):
        return p[0]

    @_("INT_T '(' expr ')'",
       "FLOAT_T '(' expr ')'")
    def expr(self, p):
        return TypeCast(p[0], p[2])
    
    @_("expr { ',' expr }")
    def exprlist(self, p):
        return [p.expr0] + [p.expr1]
    
    @_("expr '<' expr",
       "expr '>' expr",
       "expr MEI expr",
       "expr MAI expr",
       "expr II expr",
       "expr DI expr")
    def relation(self, p):
        return Relation(p[1], p[0], p[2])
    
    @_("relation AND relation",
       "relation OR relation")
    def  relation(self, p):
        return Relation(p[1], p[0], p[2])
    
    @_("NOT relation ")
    def  relation(self, p):
        return Relation(p[0], p[1])
    
    @_("'(' relation ')'")
    def  relation(self, p):
        return p.relation

    @_("NAME ':'  INT_T [ '[' expr ']' ]",
       "NAME ':'  FLOAT_T [ '[' expr ']' ]")
    def  arg(self, p):
        return Argument(p[0], p[2], p.expr)
        
    @_("arg { ',' arg }")
    def  arglist(self, p):
        return [p.arg0] + [ p.arg1 ]
    
    @_("arg ';' { locals }",
       "function ';' { locals }")
    def locals(self, p):
        return p.locals + [p[0]]
    
    @_("NAME")
    def location(self, p):
        return SimpleLocation(p[0])
        
    @_("NAME '[' expr ']'")
    def location(self, p):
        return ArrayLocation(p[0], p[2])
    
    @_("INT")
    def num(self, p):
        return Integer(p.int)
    
    @_("FLOAT")
    def num(self, p):
        return Float(p.float)

if __name__ == '__main__':
    p = Parser()
    lex=Lexer()
    p.parse(lex.tokenize)