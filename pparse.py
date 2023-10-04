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
        
        function_name = p.name
        arguments = p.arguments
        locals = p.locals
        statements = p.statements

        function_definition = {
            "type": "function",
            "name": function_name,
            "arguments": arguments,
            "locals": locals,
            "body": statements  }

        return function_definition
    
   
    @_("statement (';' statement)*")
    def statements(self, p):
        statements_sequence = [p[0]]  # Inicialmente, agregamos la primera declaración a la lista
        for statement in p[2]:
            statements_sequence.append(statement)

        return statements_sequence
    
    @_("'WHILE' relation 'do' statement")
    def statement(self, p):
        condition = p[0]  # La condición a evaluar
        body = p[3]       # El cuerpo del bucle (declaraciones que se ejecutan mientras la condición sea verdadera)

        while_loop = {
            "type": "while",
            "condition": condition,
            "body": body
        }

        return while_loop
    @_("'if' relation 'then' statement 'else' statement")
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

    @_("location ':''=' expr")
    def statement(self, p):
        # p[1] contiene la ubicación (location) a la que se asignará el valor
        location = p[1]
        # p[3] contiene la expresión cuyo valor se asignará a la ubicación
        expression = p[3]
        return {"assignment": {"location": location, "value": expression}}
    @_("'print''('literal')'")
    def statement(self, p):
        return p[2]
    @_("'write''('expr')'")
    def statement(self, p):
        return {"write": p[2]}
    @_("'read''('location')'")
    def statement(self, p):
        return {"read": p[2]}
    @_("'return' expr")
    def statement(self, p):
        return {"return": p[1]}
        
    @_("name'('exprlist')'")
    def statement(self, p):
        ...
    @_("'skip'")
    def statement(self, p):
        return {"skip": True}
    @_("'break'")
    def statement(self, p):
        return {"break": True}
    @_("'begin' statements 'end'")
    def statement(self, p):
        blok_estatements =p[1]
        return blok_estatements
        
   
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
        function_call = {
        "type": "function_call",  # Puedes usar una cadena para identificar el tipo de operación
        "name": p[0],             # El nombre de la función o método
        "arguments": p[2]         # La lista de argumentos (resultado de exprlist)
        }
        return function_call
    @_( "name")
    def expr(self, p):
       # Variable name
        if isinstance(p[0], str):
            result = p[0]
        return result
    @_( "name '[' int ']'")
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
        expresion=[p[0]]
        for expr in p[2]:
            expresion.append(expr)
        return expresion
    
    @_("relation 'and' relation","relation 'or' relation")
    def  relation(self, p):
        if p[1] == 'and':
            result = p[0] and p[2]
        elif p[1] == 'or':
            result = p[0] or p[2]
        return result
    @_("'NOT' relation ")
    def  relation(self, p):
        result = not p[1]
        return result
    @_("'(' relation ')'")
    def  relation(self, p):
        return p[1]
    @_("expr '>' expr",
       "expr '<' expr,", 
       "expr '>=' expr",
       "expr '<=' expr",
       "expr '==' expr",
       "expr '!=' expr)")
    def relation(self, p):
        if p[1] == '>':
            result = p[0] > p[2]
        elif p[1] == '<':
            result = p[0] < p[2]
        elif p[1] == '>=':
            result = p[0] >= p[2]
        elif p[1] == '<=':
            result = p[0] <= p[2]
        elif p[1] == '==':
            result = p[0] == p[2]
        elif p[1] == '!=':
            result = p[0] != p[2]

        return result
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
        valor = p[2]
        return {"array_declaration": {"type": "INT", "size": valor}}
    @_("'FLOAT' '[' float ']'") 
    def array(self, p):
        valor= p[2] 
        return {"array_declaration": {"type": "FLOAT", "size": valor}}
        
    @_("[a-zA-Z_]+[0-9-a-zA-Z_]*") 
    def name(self, p):
        return p
        
    @_(".*")
    def  literal(self, p):
        return p
   

    
 

if __name__ == '__main__':
    p = Parser()
    lex=Lexer()
    p.parse(lex.tokenize)