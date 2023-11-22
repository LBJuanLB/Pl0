'''
basparser

Analizador Lexico para el lenguaje BASIC Darmounth 64
'''
from dataclasses import asdict
import logging
import sly
from arbol import *
from plex import Lexer
from dot import *

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
        return p.funclist + [p.function]
    
    @_("function")
    def funclist(self, p):
        return [p.function]
    
    @_("FUN NAME '(' [ arglist ] ')' [ locals ] BEGIN statements END")
    def function(self, p):
        function_name = p.NAME
        arguments = p.arglist
        locals = p.locals
        statements = p.statements

        return Function(function_name, arguments, locals, statements,None)
    
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
        return If(p.relation, p.statement0, p.statement1)

    @_("location ASIG expr")
    def statement(self, p):
        return Assing(p.location, p.expr,None)
    
    @_("PRINT '(' LITERAL ')'")
    def statement(self, p):
        return Print(p[2])
    
    @_("WRITE '(' expr ')'")
    def statement(self, p):
        return Write(p.expr, None)
    
    @_("READ '(' location ')'")
    def statement(self, p):
        return Read(p.location, None)
    
    @_("RETURN expr")
    def statement(self, p):
        return Return(p.expr, None)
        
    @_("NAME '(' exprlist ')'")
    def statement(self, p):
        return FunCall(p[0], p[2],None )

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
        return Binary(p[1], p[0], p[2],None)
    
    @_("SUB expr",
       "ADD expr")
    def expr(self, p):
        return Unary(p[0], p.expr,None)

    @_( "'(' expr ')'")
    def expr(self, p):
        return p.expr

    @_("NAME '[' expr ']'")
    def expr(self, p):
        return ArrayLocation(p[0], p[2],None)

    @_("NAME '(' exprlist ')'")
    def expr(self, p):
        return FunCall(p[0], p[2],None)

    @_("NAME")
    def expr(self, p):
        return SimpleLocation(p[0],None)

    @_("INT")
    def expr(self, p):
        return Integer(p[0],SimpleType("int"))
    
    @_("FLOAT")
    def expr(self, p):
        return Float(p[0],SimpleType("float"))

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
        return Relation(p[1], p[0], p[2],None)
    
    @_("relation AND relation",
       "relation OR relation")
    def  relation(self, p):
        return Relation(p[1], p[0], p[2],None)
    
    @_("NOT relation ")
    def  relation(self, p):
        return Relation(p[0], p[1], None)
    
    @_("'(' relation ')'")
    def  relation(self, p):
        return p.relation

    @_("NAME ':'  INT_T [ '[' expr ']' ]",
       "NAME ':'  FLOAT_T [ '[' expr ']' ]")
    def  arg(self, p):
        if p.expr != None:
           return Argument(p[0], ArrayType(p[2], p.expr))
        else:
              return Argument(p[0], SimpleType(p[2])) 
        
    @_("arglist ',' arg")
    def  arglist(self, p):
        return p.arglist + [p.arg]
    
    @_("arg")
    def  arglist(self, p):
        return [p.arg]
    
    @_("locals arg ';' ",
       "locals function ';'")
    def locals(self, p):
        return p.locals + [p[1]]
    
    @_("arg ';' ",
       "function ';'")
    def locals(self, p):
        return [p[0]]
    
    @_("NAME")
    def location(self, p):
        return SimpleLocation(p[0],None)
        
    @_("NAME '[' expr ']'")
    def location(self, p):
        return ArrayLocation(p[0], p[2],None)

    #ERRORES
    @_("error")
    def program(self, p):
        print(f"Error de sintaxis: No ingresó funciones. Linea {p.lineno}")

    @_("funclist error")
    def funclist(self, p):
        print(f"Error de sintaxis: No ingresó funciones. Linea {p.lineno}")

    @_("NAME")
    def funclist(self, p):
        print(f"Error de sintaxis: Una funcion debe empezar con fun. Linea {p.lineno}")

    @_("FUN error '(' [ arglist ] ')' [ locals ] BEGIN statements END")
    def function(self, p):
        print(f"Error de sintaxis: No ingresó nombre de funcion. Linea {p.lineno}")

    @_("statements error statement")
    def statements(self, p):
        print(f"Error de sintaxis: Falto el ';' para separar sentencias. Linea {p.lineno}")

    @_("error")
    def statements(self, p):
        print(f"Error de sintaxis: No ingresó sentencias. Linea {p.lineno}")

    @_("WHILE error DO statement")
    def statement(self, p):
        print(f"Error de sintaxis: Falto la condicion del while. Linea {p.lineno}")
    
    @_("IF error THEN statement [ ELSE statement ]")
    def statement(self, p):
        print(f"Error de sintaxis: Falto la condicion del if. Linea {p.lineno}")
    
    @_("location error expr")
    def statement(self, p):
        print(f"Error de sintaxis: Falto el operador de asignacion. Linea {p.lineno}")

    @_("PRINT '(' error ')'")
    def statement(self, p):
        print(f"Error de sintaxis: Falto la cadena de texto a imprimir. Linea {p.lineno}")

    @_("WRITE '(' error ')'")
    def statement(self, p):
        print(f"Error de sintaxis: Falto la expresion a imprimir. Linea {p.lineno}")
    
    @_("READ '(' error ')'")
    def statement(self, p):
        print(f"Error de sintaxis: Falto la variable a leer. Linea {p.lineno}")
    
    @_("RETURN error")
    def statement(self, p):
        print(f"Error de sintaxis: Falto la expresion a retornar. Linea {p.lineno}")
    

    @_("BEGIN error END")
    def statement(self, p):
        print(f"Error de sintaxis: Un begin no puede estar sin sentencias. Linea {p.lineno}")
    
    @_("expr error expr")
    def expr(self, p):
        print(f"Error de sintaxis: Falto el operador. Linea {p.lineno}")
    
    @_("SUB error",
         "ADD error")
    def expr(self, p):
        print(f"Error de sintaxis: Falto la expresion. Linea {p.lineno}")   
    
    @_("'(' error ')'")
    def expr(self, p):
        print(f"Error de sintaxis: Falto la expresion. Linea {p.lineno}")

    @_("NAME '[' error ']'")
    def expr(self, p):
        print(f"Error de sintaxis: Falto la expresion en el llamado de lista. Linea {p.lineno}")

    @_("INT_T '(' error ')'",
       "FLOAT_T '(' error ')'")
    def expr(self, p):
        print(f"Error de sintaxis: Falto la expresion en el casteo. Linea {p.lineno}")

    @_("exprlist error expr")
    def exprlist(self, p):
        print(f"Error de sintaxis: Falto la ',' expresion en la lista de expresiones. Linea {p.lineno}")

    @_("error")
    def exprlist(self, p):  
        print(f"Error de sintaxis: Falto la expresion en la lista de expresiones. Linea {p.lineno}")

    @_("expr '<' error",
         "expr '>' error",
         "expr MEI error",
         "expr MAI error",
         "expr II error",
         "expr DI error")
    def relation(self, p):
        print(f"Error de sintaxis: Falto la expresion izq. Linea {p.lineno}")

    @_("error '<' expr",
         "error '>' expr",
         "error MEI expr",
         "error MAI expr",
         "error II expr",
         "error DI expr")
    def relation(self, p):
        print(f"Error de sintaxis: Falto la expresion der. Linea {p.lineno}")
    
    @_("relation error relation")
    def  relation(self, p):
        print(f"Error de sintaxis: Falto el operador AND u OR. Linea {p.lineno}")
    
    @_("NOT error")
    def  relation(self, p):
        print(f"Error de sintaxis: Falto la relacion a negar. Linea {p.lineno}")

    @_("'(' error ')'")
    def  relation(self, p):
        print(f"Error de sintaxis: Falto la relacion. Linea {p.lineno}")

    @_("NAME ':'  INT_T error",
         "NAME ':'  FLOAT_T error")
    def  arg(self, p):
        print(f"Error de sintaxis: Falto la expresion en el argumento. Linea {p.lineno}")

    @_("arglist error arg")
    def  arglist(self, p):
        print(f"Error de sintaxis: Falto la ',' en la lista de argumentos. Linea {p.lineno}")

    @_("error")
    def  arglist(self, p):
        print(f"Error de sintaxis: Falto el argumento. Linea {p.lineno}")

    @_("arg ';' error",
        "function ';' error")
    def locals(self, p):
        print(f"Error de sintaxis: Falto la declaracion de variables. Linea {p.lineno}")

    @_("error")
    def locals(self, p):
        print(f"Error de sintaxis: Falto la declaracion de variables. Linea {p.lineno}")
    
    @_("error")
    def location(self, p):
        print(f"Error de sintaxis: Error al llamar la variable. Linea {p.lineno}")

    @_("NAME '[' error ']'")
    def location(self, p):
        print(f"Error de sintaxis: Error al llamar la variable. Linea {p.lineno}")


def gen_ast(argv):
    '''
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)
    '''
    lex = Lexer()
    pas = Parser()
    
    #txt = open(argv[1]).read()
    ast = pas.parse(lex.tokenize(argv))
    return ast , Dot.render(ast)
    '''
    #Imprimir AST en consola
    print_ast(ast)
    #Imprimir AST en Graphviz
    with open('graph.dot','w') as archivo:
        archivo.write(str(Dot.render(ast)))
    '''
    
def print_ast(node, indent=0):

  if indent == 0:
    print(":::: Parse Tree ::::")

  print("  " * indent, end="")

  if isinstance(node, Program):
    print("program")

  else:
    print("+-- " + type(node).__name__)

  for name, value in vars(node).items():

    if isinstance(value, node):
      print_ast(value, indent + 2)

    elif isinstance(value, list):
      for item in value:
        print_ast(item, indent + 2)

    else:
      print("  " * (indent + 2), end="")
      print("|-- " + name, end="") 
      print(" (" + str(value) + ")")
'''
if __name__ == '__main__':
    from sys import argv
    main(argv)
'''