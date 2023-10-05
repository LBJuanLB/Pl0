from dataclasses import dataclass
from multimethod import multimeta

class  Visitor(metaclass=multimeta):
    ...
@dataclass
class Node:
    def accept(self,v:Visitor,*args, **kwargs):
        return v.visit(self, *args,**kwargs)
@dataclass
class Expression(Node):
    ...
@dataclass
class Binary(Expression):
    op :str
    lefth: Expression
    rigth: Expression
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
        left=n.lefth.accept(n.lefth)
        rigth=n.rigth.accept(n.rigth)
        return eval(f"{left}{n.op}{rigth}")

