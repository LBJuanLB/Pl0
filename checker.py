from arbol import *
from typesys import *
# ---------------------------------------------------------------------
#  Tabla de Simbolos
# ---------------------------------------------------------------------
class Symtab:
    '''
    Una tabla de símbolos.  Este es un objeto simple que sólo
    mantiene una hashtable (dict) de nombres de simbolos y los
    nodos de declaracion o definición de funciones a los que se
    refieren.
    Hay una tabla de simbolos separada para cada elemento de
    código que tiene su propio contexto (por ejemplo cada función,
    clase, tendra su propia tabla de simbolos). Como resultado,
    las tablas de simbolos se pueden anidar si los elementos de
    código estan anidados y las búsquedas de las tablas de
    simbolos se repetirán hacia arriba a través de los padres
    para representar las reglas de alcance léxico.
    '''
    class SymbolDefinedError(Exception):
        '''
        Se genera una excepción cuando el código intenta agregar
        un simbol a una tabla donde el simbol ya se ha definido.
        Tenga en cuenta que 'definido' se usa aquí en el sentido
        del lenguaje C, es decir, 'se ha asignado espacio para el
        simbol', en lugar de una declaración.
        '''
        pass

    def __init__(self, parent=None):
        '''
        Crea una tabla de símbolos vacia con la tabla de
        simbolos padre dada.
        '''
        self.entries = {}
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []

    def add(self, name, value):
        '''
        Agrega un simbol con el valor dado a la tabla de simbolos.
        El valor suele ser un nodo AST que representa la declaración
        o definición de una función, variable (por ejemplo, Declaración
        o FuncDeclaration)
        '''
        if name in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[name] = value

    def get(self, name):
        '''
        Recupera el símbol con el nombre dado de la tabla de
        simbol, recorriendo hacia arriba a traves de las tablas
        de simbol principales si no se encuentra en la actual.
        '''
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None

class Checker(Visitor):

    def visit(self, n: Program, env: Symtab):
        # Crear un nuevo contexto (Symtab global)
        Table = Symtab()
        # Visitar cada una de las declaraciones asociadas
        for funt in n.funlist:
            funt.accept(self, Table)

    def visit(self, n: Function, env: Symtab):
        # Agregar el nombre de la funcion a Symtab
        env.add(n.name, n)
        # Crear un nuevo contexto (Symtab)
        Table = Symtab(env)
        # Visitar ParamList
        if n.arguments != None:
            for arg in n.arguments:
                arg.accept(self, Table)
        # Visitar VarList
        if n.locals != None:
            for local in n.locals:
                local.accept(self, Table)
        # Visitar StmtList
        if n.statements != None:
            for stmt in n.statements:
                stmt.accept(self, Table)
                 # Determinar el datatype de la funcion (revisando instrucciones return)
                if isinstance(stmt, Return):
                    datatype=stmt.datatype
        return datatype

    def visit(self, n: Name, env: Symtab):
        # Buscar el nombre en Symtab
        nombre=env.get(n.name)
        if nombre == None:
            raise TypeError(f'No se encuentra {n.name}')

    def visit(self, n: Literal, env: Symtab):
        # Devolver datatype
        return n.datatype.name
    
    def visit(self, n: Location, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        node = env.get(n.name)
        if node == None:
            raise TypeError(f'No se encuentra {n.name}')
        # Devuelvo el datatype
        return node.datatype

    def visit(self, n: TypeCast, env: Symtab):
        # Visitar la expresion asociada
        n.expr.accept(self, env)
        # Devolver datatype asociado al nodo
        return n.datatype.name
    
    def visit(self, n: Relation, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        izq = n.left.accept(self, env)
        # Visitar el hijo derecho (devuelve datatype)
        der = n.right.accept(self, env)
        # Comparar ambos tipo de datatype
        datatype=check_binary_op(n.op, izq, der)
        if datatype == None:
            raise TypeError(f'No se puede operar {izq} con {der}')
        else:
            return datatype

    def visit(self, n: FunCall, env: Symtab):
        # Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
        node = env.get(n.name)
        #Tipo de retorno
        datatype=node.datatype
        #Num Parametros
        NumParm=len(node.arguments)   
        # Visitar la lista de Argumentos
        listdtype=[]
        if n.exprlist != None:
            for arg in n.exprlist:
                listdtype.append(arg.accept(self, env))
        # Comparar el numero de argumentos con parametros
        if NumParm != len(n.exprlist):
            raise TypeError(f'Numero de argumentos incorrecto')
        # Comparar cada uno de los tipos de los argumentos con los parametros
        j=0
        for i in node.arguments:
            if i.datatype != listdtype[j]:
                raise TypeError(f'Argumento incorrecto')
            j+=1
        # Retornar el datatype de la funcion
        return datatype

    def visit(self, n: Binary, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        izq = n.left.accept(self, env)
        # Visitar el hijo derecho (devuelve datatype)
        der = n.right.accept(self, env)
        # Comparar ambos tipo de datatype
        datatype=check_binary_op(n.op, izq, der)
        if datatype == None:
            raise TypeError(f'No se puede operar {izq} con {der}')
        else:
            n.datatype=datatype
            env.add(n.name, n)
            return datatype

    def visit(self, n: Relation, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        izq=n.left.accept(self, env)
        # Visitar el hijo derecho (devuelve datatype)
        der=n.right.accept(self, env)
        # Comparar ambos tipo de datatype
        datatype=check_binary_op(n.op, izq, der)
        if datatype == None:
            raise TypeError(f'No se puede operar {izq} con {der}')
        else:
            n.datatype=datatype
            env.add(n.name, n)
            return datatype

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        data_type_expr=n.expr.accept(self, env)
        # Comparar datatype
        datatype=check_unary_op(n.op, data_type_expr)
        if datatype == None:
            raise TypeError(f'No se puede operar {data_type_expr}')
        else:
            n.datatype=datatype
            env.add(n.name, n)
            return datatype

    def visit(self, n: Argument, env: Symtab):
        # Agregar el nombre del parametro a Symtab
        env.add(n.name, n)
        return n.datatype

    def visit(self, n: Print, env: Symtab):
        ...     

    def visit(self, n: Write, env: Symtab):
        # Buscar la Variable en Symtab
        nodo=env.get(n.expr.name)
        if nodo == None:
            raise TypeError(f'No se encuentra {n.expr.name}')
        else:
            return nodo.datatype
    def visit(self, n: Read, env: Symtab):
        # Buscar la Variable en Symtab
        nodo=env.get(n.expr.name)
        if nodo == None:
            raise TypeError(f'No se encuentra {n.expr.name}')
        else:
            return nodo.datatype

    def visit(self, n: While, env: Symtab):
        # Visitar la condicion del While (Comprobar tipo bool)
        condition_type = n.relation.accept(self, env)
        if condition_type != 'bool':
            raise TypeError(f'Tipo incorrecto para la condición del While. Se esperaba "bool", pero se encontró "{condition_type}".')

        # Visitar las Stmts
        for stmt in n.statement:
            stmt.accept(self, env)
        

    def visit(self, n: Break, env: Symtab):
        # Esta dentro de un While?
        current_env = env
        while current_env is not None:
            if isinstance(current_env, While):
                return True
                
        #current_env = current_env.parent
        raise ValueError('La instrucción "Break" debe estar dentro de un bucle "While".')

    def visit(self, n: If, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        condition_type = n.relation.accept(self, env)
        if condition_type != 'bool':
            raise TypeError(f'Tipo incorrecto para la condición del If. Se esperaba "bool", pero se encontró "{condition_type}".')

        # Visitar las Stmts del then
        for stmt in n.statement:
            stmt.accept(self, env)

        # Visitar las Stmts del else, si existen
        if n.if_else is not None:
            for stmt in n.if_else:
                stmt.accept(self, env)
        

    def visit(self, n: Return, env: Symtab):
        # Visitar la expresion asociada
        expr_type = n.expr.accept(self, env)
        # Actualizar el datatype de la funcion
        n.datatype = expr_type
        env.add(n.name, n)
        return expr_type
            

    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: Begin, env: Symtab):
        # Visitar cada una de las instruciones asociadas
        for stmt in n.statements:
            stmt.accept(self, env)

