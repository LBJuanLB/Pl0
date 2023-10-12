# pparse.py
'''
La libreria SLY permite gramaticas en EBNF. 
    {} repeticion 0 o mas.
    [] opcionalidad
'''
import sly

class Parser(sly.Parser):
    '''
    '''
    debugfile='pl0.tx'

    @_("funclist")
    def program(self, p):
        ...

    @_("function { function }")
    def funclist(self, p):
        ...

    @_("FUN ID parmlist varlist BEGIN stmtlist END")
    def function(self, p):
        ...

    @_("'(' [ parmlistitems ] ')'")
    def parmlist(self, p):
        ...

    @_("parm { ',' parm }")
    def parlistitems(self, p):
        ...

    @_("ID ':' typename")
    def parm(self, p):
        ...

    @_("INT [ '[' expr ']' ]", "FLOAT [ '[' expr ']' ]")
    def typename(self, p):
        ...

    @_("[ declist optsemi ]")
    def varlist(self, p):
        ...

    @_("vardecl { ';' vardecl }")
    def declist(self, p):
        ...

    @_("parm", "function")
    def vardecl(self, p):
        ...

    @_("stmt { ';' stmt }")
    def stmtlist(self, p):
        ...

    @_("PRINT '(' STRING ')'",
       "WRITE '(' expr ')'",
       "READ '(' location ')'",
       "WHILE relop DO stmt",
       "BREAK",
       "IF relop THEN stmt [ ELSE stmt ]",
       "BEGIN stmtlist END",
       "location ':=' expr",
       "RETURN expr",
       "SKIP",
       "ID '(' exprlist ')'")
    def stmt(self, p):
        ...

    @_("ID [ '[' expr ']' ]")
    def location(self, p):
        ...

    @_("[ exprlistitems ]")
    def exprlist(self, p):
        ...

    @_("expr { ',' expr }")
    def exprlistitems(self, p):
        ...

    @_("expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr",
       "'-' expr",
       "'+' expr",
       "'(' expr ')'",
       "INUMBER",
       "FNUMBER",
       "ID [ '[' expr ']']",
       "ID '(' exprlist ')'",
       "INT '(' expr ')'",
       "FLOT '(' expr ')'")
    def expr(self, p):
        ...
    
    @_("expr LT expr",
       "expr LE expr",
       "expr GT expr",
       "expr GE expr",
       "expr EQ expr",
       "expr NE expr",
       "relop AND relop",
       "relop OR relop",
       "NOT relop")
    def relop(self, p):
        ...
