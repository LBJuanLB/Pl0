from dataclasses import dataclass
from multimethod import multimeta
class  Visitor(multimeta):
    ...
@dataclass
class Node:
    def accept(self,n:Visitor,*args, **kwargs):
        ...
@dataclass
class Expression(Node):
    ...
@dataclass
class Binary(Expression):
    ...
@dataclass
class lefth(Binary):
    ...
@dataclass
class rigth(Binary):
    ...
    
@dataclass
class Number(Expression):
    value: int
class Eval(Visitor):
    @classmethod
    def eval(cls,n:Node):
        v=cls()
        return n.accept(v)
    def visit(self, n:Number):
        return n.value
    def visit(self, n:Binary):
        left=n.accept(n.lefth)
        rigth=n.accept(n.rigth)
        