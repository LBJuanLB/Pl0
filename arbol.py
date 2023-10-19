from plex import *

class node :
    ...
class Statement(node):
    ...
class DataType(node):
    ...
class Location(node):
    ...
class Expression(node):
    ...

class Program (Statement):
    funlist: list


class Declaration(Statement):
    ...
class Funtion (Declaration):
    name: Name
    arguments: list
    locals: list
    statements: list
    
class Assign(Statement):
    location: Location
    expr: Expression
    
class Print(Statement):
    string: str
    
class Write(Statement):
    expr: Expression
    
class Read(Statement):
    local:Location
class While(Statement):
    relation: Relation
    statement: Statement
    
class Break(Statement):
    ...
class IF(Statement):
    relation: Relation
    statement: Statement
    if_else : Statement
class Return(Statement):
    expr: Expression
class Skipe(Statement):
    ...
class SimpleType(DataType):
    name: Name
class ArrayType(DataType):
    name: Name
    expr: Expression
    
class SimpleLocation(Location):
    ...
class ArrayLocation(Location):
    ...
class Literal(Expression):
    cadena: str 
class TypeCast(Expression):
    ...
class Assign (Expression):
    ...
class FunCall(Expression):
    ...
