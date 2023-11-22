from arbol import *
from symtab import *

class AST(Visitor):
    def __init__(self):
        self.registros=0
        self.whiles=0
        self.ifs=0
    @classmethod
    def instrucciones(cls, n:node):
        lista = []
        inst = cls()
        return n.accept(inst, lista)
    
    def visit(self, n:Program, inst:list):
        for funt in n.funlist:
            funt.accept(self, inst)
        return inst
    
    def visit(self, n:Function, inst:list):
        #Se crea el label de la funcion
        inst.append(('LABEL', n.name))
        if n.arguments != None:
            for arg in n.arguments:
                arg.accept(self, inst)
        if n.locals != None:
            for local in n.locals:
                local.accept(self, inst)
        if n.statements != None:
            for stmt in n.statements:
                stmt.accept(self, inst)

    def visit(self, n:Name, inst:list):
        return n.name

    def visit(self, n:Integer, inst:list):

        #Cargamos el valor del entero en el registro
        self.registros+=1
        inst.append(('MOVI', n.value, f'R{self.registros}'))
        return f'R{self.registros}', 'int'
    
    def visit(self, n:Float, inst:list):
        #Cargalos el valor del float en el registro
        self.registros+=1
        inst.append(('MOVF', n.value, f'R{self.registros}'))
        return f'R{self.registros}', 'float'
    
    def visit(self, n:Relation, inst:list):
        #Se cargan los valores de las expresiones en los registros
        left,tipoL = n.left.accept(self, inst)
        right,tipoR = n.right.accept(self, inst)
        #Se crea la instruccion de comparacion
        self.registros+=1
        if tipoL == 'int':
            inst.append(('CMPI',n.op, left, right,f'R{self.registros}'))
            return f'R{self.registros}', 'int'
        elif tipoL == 'float':
            inst.append(('CMPF',n.op, left, right,f'R{self.registros}'))
            return f'R{self.registros}', 'float'
    
    def visit(self, n:Assing, inst:list):
        #Se cargan los valores de la expresion en el registro
        expr, tipoExpr = n.expr.accept(self, inst)
        if tipoExpr == 'int':
            #Se crea la instruccion de asignacion
            inst.append(('STOREI', expr, n.location.name))

        elif tipoExpr == 'float':
            #Se crea la instruccion de asignacion
            inst.append(('STOREF', expr, n.location.name))
        
    def visit(self, n:Print, inst:list):
        ...
    
    def visit(self, n:Write, inst:list):
        #Se cargan los valores de la expresion en el registro
        expr, tipoExpr = n.expr.accept(self,inst)
        if tipoExpr == 'int':
            #Se crea la instruccion de print
            inst.append(('PRINTI', expr))
        elif tipoExpr == 'float':
            #Se crea la instruccion de print
            inst.append(('PRINTF', expr))

    def visit(self, n:Read, inst:list):
        ...
    
    def visit(self, n:While, inst:list):
        self.whiles+=1
        #Se crea el label del while
        inst.append(('LABEL', f'WHILE_{self.whiles}'))
        #Se cargan los valores de la expresion en el registro
        expr, tipoExpr = n.relation.accept(self,inst)
        #Se crea la instruccion de comparacion
        inst.append(('CBRANCH', expr, f'TRUE_WHILE_{self.whiles}',f'END_WHILE_{self.whiles}',))
        #Se crea el label de verdadero del while
        inst.append(('LABEL', f'TRUE_WHILE_{self.whiles}'))
        #Se cargan los valores de las expresiones en los registros  
        n.statement.accept(self, inst)
        #Se crea la instruccion de salto
        inst.append(('BRANCH', f'WHILE_{self.whiles}'))
        #Se crea el label de fin del while
        inst.append(('LABEL', f'END_WHILE_{self.whiles}'))

    
    def visit(self, n:If, inst:list):
        self.ifs+=1
        #Se cargan los valores de la expresion en el registro
        expr, tipoExpr = n.relation.accept(self, inst)
        if n.if_else != None:
            #Se crea la instruccion de comparacion
            inst.append(('CBRANCH', expr, f'TRUE_IF_{self.ifs}',f'ELSE_IF_{self.ifs}',))
            #Se crea el label de verdadero del if
            inst.append(('LABEL', f'TRUE_IF_{self.ifs}'))
            #Se cargan los valores de las expresiones en los registros  
            n.statement.accept(self, inst)
            #Se crea la instruccion de salto
            inst.append(('BRANCH', f'END_IF_{self.ifs}'))
            #Se crea el label de falso del if
            inst.append(('LABEL', f'ELSE_IF_{self.ifs}'))
            #Se cargan los valores de las expresiones en los registros  
            n.if_else.accept(self, inst)
            #Se crea el label de fin del if
            inst.append(('LABEL', f'END_IF_{self.ifs}'))
        else:
            #Se crea la instruccion de comparacion
            inst.append(('CBRANCH', expr, f'TRUE_IF_{self.ifs}',f'END_IF_{self.ifs}',))
            #Se crea el label de verdadero del if
            inst.append(('LABEL', f'TRUE_IF_{self.ifs}'))
            #Se cargan los valores de las expresiones en los registros  
            n.statement.accept(self, inst)
            #Se crea el label de fin del if
            inst.append(('LABEL', f'END_IF_{self.ifs}'))

    def visit(self, n:Return, inst:list):
        expr, tipoExpr = n.expr.accept(self, inst)
        if tipoExpr == 'int':
            #Se crea la instruccion de return
            inst.append(('RETI', expr))
        elif tipoExpr == 'float':
            #Se crea la instruccion de return
            inst.append(('RETF', expr))
    
    def visit(self,n:Skip, inst:list):
        ...
    
    def visit(self,n:Break, inst:list):   
        ...
    
    def visit(self, n:Begin, inst:list):
        for stmt in n.statements:
            stmt.accept(self, inst)
    
    def visit(self, n:SimpleType,inst:list):
        return n.name
    
    def visit(self, n:ArrayType,inst:list):
        return n.name, n.expr.value
    
    def visit(self, n:SimpleLocation,inst:list):
        if n.datatype.name == 'int':
            self.registros+=1
            inst.append(('LOADI', n.name, f'R{self.registros}'))
            registro = f'R{self.registros}'
            return registro, n.datatype.name
        elif n.datatype.name == 'float':
            self.registros+=1
            inst.append(('LOADF', n.name, f'R{self.registros}'))
            registro = f'R{self.registros}'
            self.registros+=1
            return registro, n.datatype.name
    
    def visit(self, n:ArrayLocation,inst:list):
        Rexpr, TipoExpr = n.expr.accept(self,inst)
        inst.append(('LOADI'))  
        return n.name, n.expr.value, n.datatype.name

    def visit(self, n:Binary, inst:list):
        #Se cargan los valores de las expresiones en los registros
        left, tipoL = n.left.accept(self,inst)
        right, tipoR = n.right.accept(self,inst)
        #Se crea la instruccion de operacion
        self.registros+=1
        if tipoL == 'int':
            if n.op == '+':
                inst.append(('ADDI', left, right, f'R{self.registros}'))
            elif n.op == '-':
                inst.append(('SUBI', left, right, f'R{self.registros}'))
            elif n.op == '*':
                inst.append(('MULI', left, right, f'R{self.registros}'))
            elif n.op == '/':
                inst.append(('DIVI', left, right, f'R{self.registros}'))    
            return f'R{self.registros}', 'int'
        elif tipoL == 'float':
            if n.op == '+':
                inst.append(('ADDF', left, right, f'R{self.registros}'))
            elif n.op == '-':
                inst.append(('SUBF', left, right, f'R{self.registros}'))
            elif n.op == '*':
                inst.append(('MULF', left, right, f'R{self.registros}'))
            elif n.op == '/':
                inst.append(('DIVF', left, right, f'R{self.registros}'))
            return f'R{self.registros}', 'float'
    
    def visit(self, n:Unary, inst:list):
        #Se cargan los valores de la expresion en el registro
        expr, tipoExpr = n.expr.accept(self,inst)
        #Se crea la instruccion de operacion
        self.registros+=1
        if tipoExpr == 'int':
            if n.op == '-':
                inst.append(('MOVI', 0, f'R{self.registros}'))
                inst.append(('SUBI', f'R{self.registros}', expr, f'R{self.registros+1}'))
                self.registros+=1
            elif n.op == '+':
                inst.append(('MOVI', 0, f'R{self.registros}'))
                inst.append(('ADDI', f'R{self.registros}', expr, f'R{self.registros+1}'))
                self.registros+=1
            return f'R{self.registros}', 'int'
        elif tipoExpr == 'float':
            if n.op == '-':
                inst.append(('MOVF', 0, f'R{self.registros}'))
                inst.append(('SUBF', f'R{self.registros}', expr, f'R{self.registros+1}'))
                self.registros+=1
            elif n.op == '+':
                inst.append(('MOVF', 0, f'R{self.registros}'))
                inst.append(('ADDF', f'R{self.registros}', expr, f'R{self.registros+1}'))
                self.registros+=1
            return f'R{self.registros}', 'float'
    
    def visit(self, n:Argument, inst:list):
        if n.datatype.name == 'int':
            #Se crea la instruccion de declaracion
            inst.append(('VARI', n.name))
        elif n.datatype.name == 'float':
            #Se crea la instruccion de declaracion
            inst.append(('VARF', n.name))
    
    def visit(self, n:TypeCast, inst:list):    
        expr, tipoExpr = n.expr.accept(self,inst)
        if n.datatype.name == 'int':
            #Se crea la instruccion de casteo
            self.registros+=1
            inst.append(('ITOF', expr, f'R{self.registros}'))
            return f'R{self.registros}', 'float'
        elif n.datatype.name == 'float':
            #Se crea la instruccion de casteo
            self.registros+=1
            inst.append(('FTOI', expr, f'R{self.registros}'))
            return f'R{self.registros}', 'int'
    
    def visit(self, n:FunCall, inst:list):
        funcion=['CALL',n.name]
        for expr in n.exprlist:
            registro, tipo = expr.accept(self, inst)
            funcion.append(registro)
        #Se crea la instruccion de llamada
        self.registros+=1
        funcion.append(f'R{self.registros}')
        inst.append(tuple(funcion))
        return f'R{self.registros}', n.datatype.name