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

class Name(Expression):
    name: str

class Num(Expression):
    ...

class Integer(Num):
    value: int

class Float(Num):
    value: float

class Relation(Expression):
    op: str
    left: Expression
    right: Expression

class Funtion(Declaration):
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

class If(Statement):
    relation: Relation
    statement: Statement
    if_else : Statement

class Return(Statement):
    expr: Expression

class Skip(Statement):
    ...

class Break(Statement):
    ...

class Begin(Statement):
    statements: list

class SimpleType(DataType):
    name: Name

class ArrayType(DataType):
    name: Name
    expr: Expression
    
class SimpleLocation(Location):
    name: Name

class ArrayLocation(Location):
    name: Name
    expr: Expression

class Literal(Expression):
    cadena: str 

class Binary(Expression):
    op: str
    left: Expression
    right: Expression

class Unary(Expression):
    op: str
    expr: Expression

class Argument(Expression):
    name: Name
    datatype: DataType

class TypeCast(Expression):
    ...

class FunCall(Expression):
    name: Name
    exprlist: list
