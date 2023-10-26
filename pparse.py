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
    
    @_("funclist function")
    def funclist(self, p):
        return p.stmtlist + [p.function]
    
    @_("function")
    def funclist(self, p):
        return [p.function]
    
    @_("FUN NAME '(' [ arglist ] ')' locals BEGIN statements END")
    def function(self, p):
        function_name = p.NAME
        arguments = p.arglist
        locals = p.locals
        statements = p.statements

        return Funtion(function_name, arguments, locals, statements)
    
    @_("statements ';' statement")
    def statements(self, p):
        return p.statements + [p.statement]
    
    @_("statement")
    def statements(self, p):
        return [p.statement]
    
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
   
    @_("expr ADD expr",
       "expr SUB expr",
       "expr MUL expr",
       "expr DIV expr")
    def expr(self, p):
        return Binary(p[1], p[0], p[2])
    
    @_("SUB expr",
       "ADD expr")
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

    @_("INT")
    def expr(self, p):
        return Integer(p[0])
    
    @_("FLOAT")
    def expr(self, p):
        return Float(p[0])

    @_("INT_T '(' expr ')'",
       "FLOAT_T '(' expr ')'")
    def expr(self, p):
        return TypeCast(p[0], p[2])
    
    @_("exprlist ',' expr")
    def exprlist(self, p):
        return p.exprlist + [p.expr]
    
    @_("expr")
    def exprlist(self, p):
        return [p.expr]
    
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
        
    @_("arglist ',' arg")
    def  arglist(self, p):
        return p.arglist + [p.arg]
    
    @_("arg")
    def  arglist(self, p):
        return [p.arg]
    
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

def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)
    
    lex = Lexer()
    pas = Parser()
    txt = open(argv[1]).read()
    ast = pas.parse(lex.tokenize(txt))
    ##
    for tok in lex.tokenize(txt):
        #value=tok.value if isinstance(tok.value , str(tok.value))
        if isinstance(tok.value, str):
            value = tok.value
        else:
            value = tok.value
        table.add_row(tok.type,
                      str(value),
                      str(tok.lineno),
                      str(tok.index),
                      str(tok.end))
    console = Console()
    console.print(table)
    print(ast)
if __name__ == '__main__':
    from sys import argv
    main(argv)