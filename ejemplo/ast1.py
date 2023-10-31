from dataclasses import dataclass
from multimethod import multimeta
from graphviz import Diagraph
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

class Dot(Vistor):
    node_default={
        'shape':'box',
        'color':'deepskyblue',
        'style':'filled'
        }
    edge_default={
        'arrowhead':'none',
    }
    def __int__(self):
        self.dot=Diagraph('AST')
        self.dot.attr('node',**self.node_default)
        self.dot.attr('edge',**self.edge_default)
        self.seq=0
    def __str__(self):
        return self.dot.source
    def __repr__(self):
        return self.dot.source
    def name (self):
        self.seq+=1
        return f"n{self.seq:0d}"
    @classmethod
    def render(cls,n:Node):
        dot=cls()
        n.accept(dot)
        return dot.dot
    def visit(self,n:Number):
        name=self.name()
        self.dot.node(name label=f'{n.value}')
        return name
    def visit(self, n:Binary):
        name=self.name()
        self.dot.node(name label=f'{n.op}',shape='',color='')
        self.dot.edge(name.n.lefth.accept(self))
        self.dot.edge(name, n.rigth.accept(self))
        
##print (Dot.render(ast).source) capitulo 8 y capitulo 9
