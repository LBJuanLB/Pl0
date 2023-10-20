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
    debugfile = 'pl0.txt'

    tokens = Lexer.tokens

    # Implementacion Reglas de la Gramatica

    @_("funclist")
    def program(self, p):
        return p.funclist

    @_("function { function }")
    def funclist(self, p):
        return p.function

    @_("FUN name '(' [ arglist ] ')' locals BEGIN statements END")
    def function(self, p):
        function_name = p.name
        arguments = p.arglist
        locals = p.locals
        statements = p.statements

        function_definition = {
            "type": "function",
            "name": function_name,
            "arguments": arguments,
            "locals": locals,
            "body": statements}

        return function_definition
    
   
    @_("statement {';' statement}")
    def statements(self, p):
        statements_sequence = [p[0]]  # Inicialmente, agregamos la primera declaración a la lista
        for statement in p[2]:
            statements_sequence.append(statement)

        return statements_sequence
    
    @_("WHILE relation DO statement")
    def statement(self, p):
        condition = p[0]  # La condición a evaluar
        body = p[3]       # El cuerpo del bucle (declaraciones que se ejecutan mientras la condición sea verdadera)

        while_loop = {
            "type": "while",
            "condition": condition,
            "body": body
        }

        return while_loop
    @_("IF relation THEN statement [ELSE statement]")
    def statement(self, p):
        condition = p[1]      # La condición a evaluar
        true_branch = p[3]    # El bloque de código a ejecutar si la condición es verdadera
        false_branch = p[5]   # El bloque de código a ejecutar si la condición es falsa

        # Realiza acciones correspondientes a la estructura de control 'if-else'
        # Puedes tomar medidas para construir una estructura que refleje la estructura de control 'if-else',
        # incluyendo la condición, el bloque de código verdadero y el bloque de código falso.

        if_else = {
            "type": "if_else",
            "condition": condition,
            "true_branch": true_branch,
            "false_branch": false_branch
        }

        return if_else

    @_("location ':=' expr")
    def statement(self, p):
        # p[1] contiene la ubicación (location) a la que se asignará el valor
        location = p[0]
        # p[3] contiene la expresión cuyo valor se asignará a la ubicación
        expression = p[3]
        return {"assignment": {"location": location, "value": expression}}
    
    @_("PRINT '(' LITERAL ')'")
    def statement(self, p):
        return p[2]
    
    @_("WRITE '(' expr ')'")
    def statement(self, p):
        return {"write": p[2]}
    
    @_("READ '(' location ')'")
    def statement(self, p):
        return {"read": p[2]}
    
    @_("RETURN expr")
    def statement(self, p):
        return {"return": p[1]}
        
    @_("NAME '(' exprlist ')'")
    def statement(self, p):
        ...
    @_("SKIP")
    def statement(self, p):
        return {"skip": True}
    
    @_("BREAK")
    def statement(self, p):
        return {"break": True}
    
    @_("BEGIN statements END")
    def statement(self, p):
        blok_estatements =p[1]
        return blok_estatements
   
    @_("expr '+' expr",
       "expr '-' expr",
       "expr '*' expr",
       "expr '/' expr")
    def expr(self, p):
        ...
    
    @_("'-' expr",
       "'+' expr")
    def expr(self, p):
        # Operador unario 
        ...

    @_( "'(' expr ')'")
    def expr(self, p):
        # Paréntesis: '(' expr ')'
        if p[0] == '(' and p[2] == ')':
            result = p[1]
        return result

    @_("NAME '[' expr ']'")
    def expr(self, p):
        ...

    @_("NAME '(' exprlist ')'")
    def expr(self, p):
        ...

    @_("NAME")
    def expr(self, p):
        ...

    @_("NUM")
    def expr(self, p):
        ...

    @_("INT_T '(' expr ')'",
       "FLOAT_T '(' expr ')'")
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
    
    @_("expr {',' expr}")
    def exprlist(self, p):
        expresion=[p[0]]
        for expr in p[2]:
            expresion.append(expr)
        return expresion
    
    @_("expr '<' expr",
       "expr '>' expr",
       "expr '<=' expr",
       "expr '>=' expr",
       "expr '==' expr",
       "expr '!=' expr")
    def relation(self, p):
        ...
    
    @_("relation AND relation",
       "relation OR relation")
    def  relation(self, p):
        if p[1] == 'and':
            result = p[0] and p[2]
        elif p[1] == 'or':
            result = p[0] or p[2]
        return result
    
    @_("NOT relation ")
    def  relation(self, p):
        result = not p[1]
        return result
    
    @_("'(' relation ')'")
    def  relation(self, p):
        return p[1]


    @_("NAME ':'  INT_T [ '[' expr ']' ]",
       "NAME ':'  FLOAT_T [ '[' expr ']' ]")
    def  arg(self, p):
        ...
        
    @_("arg { ',' arg }")
    def  arglist(self, p):
        ...
    
    @_("arg ';' { locals }",
       "function ';' { locals }")
    def locals(self, p):
        ...
    
    @_("NAME")
    def location(self, p):
        ...
    @_("NAME '[' expr ']'")
    def location(self, p):
        ...
    
    @_("INT")
    def num(self, p):
        ...
    @_("FLOAT")
    def num(self, p):
        ...
    
    @_("((\+|-)?[1-9][0-9]*)|[0]")
    def int(self, p):
        return [p.statement] + p.statements

    @_("(\+|-)?([0]|[1-9][0-9]*)(\.[0-9]+((e|E)(\+|-)?[0-9]+)?")
    def float(self,p):
        ...
        
    @_("[a-zA-Z_]+[0-9-a-zA-Z_]*") 
    def name(self, p):
        ...
        
    @_("'\"' [^\"]* '\"'")
    def  literal(self, p):
        ...

if __name__ == '__main__':
    p = Parser()
    lex=Lexer()
    p.parse(lex.tokenize)