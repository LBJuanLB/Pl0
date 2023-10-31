from plex import *
from dataclasses import dataclass
from multimethod import multimeta

class Visitor(metaclass=multimeta):
  ...

@dataclass
class node:
  def accept(self, v:Visitor, *args, **kwargs):
    return v.visit(self, *args, **kwargs)

@dataclass
class Statement(node):
    ...

@dataclass
class DataType(node):
    ...

@dataclass
class Location(node):
    ...

@dataclass
class Expression(node):
    ...

@dataclass
class Program (Statement):
    funlist: list

@dataclass
class Declaration(Statement):
    ...

@dataclass
class Name(Expression):
    name: str

@dataclass
class Num(Expression):
    ...

@dataclass
class Integer(Num):
    value: int

@dataclass
class Float(Num):
    value: float

@dataclass
class Relation(Expression):
    op: str
    left: Expression
    right: Expression

@dataclass
class Function(Declaration):
    name: Name
    arguments: list
    locals: list
    statements: list

@dataclass    
class Assing(Statement):
    location: Location
    expr: Expression

@dataclass    
class Print(Statement):
    string: str

@dataclass    
class Write(Statement):
    expr: Expression

@dataclass    
class Read(Statement):
    local:Location

@dataclass
class While(Statement): 
    relation: Relation
    statement: Statement

@dataclass
class If(Statement):
    relation: Relation
    statement: Statement
    if_else : Statement

@dataclass
class Return(Statement):
    expr: Expression

@dataclass
class Skip(Statement):
    ...

@dataclass
class Break(Statement):
    ...

@dataclass
class Begin(Statement):
    statements: list

@dataclass
class SimpleType(DataType):
    name: Name

@dataclass
class ArrayType(DataType):
    name: Name
    expr: Expression

@dataclass    
class SimpleLocation(Location):
    name: Name

@dataclass
class ArrayLocation(Location):
    name: Name
    expr: Expression

@dataclass
class Literal(Expression):
    cadena: str 

@dataclass
class Binary(Expression):
    op: str
    left: Expression
    right: Expression

@dataclass
class Unary(Expression):
    op: str
    expr: Expression

@dataclass
class Argument(Expression):
    name: Name
    datatype: DataType

@dataclass
class TypeCast(Expression):
    dataType: DataType
    expr: Expression 

@dataclass
class FunCall(Expression):
    name: Name
    exprlist: list
