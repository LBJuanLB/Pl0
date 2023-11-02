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
        Table.__init__(self, parent=Program)
        # Visitar cada una de las declaraciones asociadas
        for funt in n.funlist:
            Table.add(funt.accept(self, Table))

    def visit(self, n: Function, env: Symtab):
        # Agregar el nombre de la funcion a Symtab
        env.add(n.name, n)
        # Crear un nuevo contexto (Symtab)
        Table = Symtab()
        Table.__init__(self, parent=Function)
        # Visitar ParamList
        if n.arguments != None:
            for arg in n.arguments:
                Table.add(arg.accept(self, Table))
        # Visitar VarList
        if n.locals != None:
            for local in n.locals:
                Table.add(local.accept(self, Table))
        # Visitar StmtList
        if n.statements != None:
            for stmt in n.statements:
                Table.add(stmt.accept(self, Table))
        # Determinar el datatype de la funcion (revisando instrucciones return)
        return Table.get(n.name)

    def visit(self, n: Name, env: Symtab):
        # Buscar el nombre en Symtab
        return env.get(n.name)

    def visit(self, n: Literal, env: Symtab):
        # Devolver datatype
        return n.accept(self, env)
    
    def visit(self, n: Location, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        node = env.get(n.name)
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
        #Num Parametros
        NumParm=len(node.arguments)   
        # Visitar la lista de Argumentos
        if n.arguments != None:
            for arg in n.arguments:
                arg.accept(self, env)
        # Comparar el numero de argumentos con parametros

        # Comparar cada uno de los tipos de los argumentos con los parametros
        # Retornar el datatype de la funcion

    def visit(self, n: Binary, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype

    def visit(self, n: Logical, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        # Visitar el hijo derecho (devuelve datatype)
        # Comparar ambos tipo de datatype

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        # Comparar datatype

    def visit(self, n: VarDefinition, env: Symtab):
        # Agregar el nombre de la variable a Symtab

    def visit(self, n: Parameter, env: Symtab):
        # Agregar el nombre del parametro a Symtab

    def visit(self, n: Print, env: Symtab):
        ...     

    def visit(self, n: Write, env: Symtab):
        # Buscar la Variable en Symtab

    def visit(self, n: Read, env: Symtab):
        # Buscar la Variable en Symtab

    def visit(self, n: While, env: Symtab):
        # Visitar la condicion del While (Comprobar tipo bool)
        # Visitar las Stmts

    def visit(self, n: Break, env: Symtab):
        # Esta dentro de un While?

    def visit(self, n: IfStmt, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        # Visitar las Stmts del then y else

    def visit(self, n: Return, env: Symtab):
        # Visitar la expresion asociada
        # Actualizar el datatype de la funcion

    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: StmtList, env: Symtab):
        # Visitar cada una de las instruciones asociadas

    def visit(self, n: VarList, env: Symtab):
        # Visitar cada una de las variables asociadas

    def visit(self, n: ParmList, env: Symtab):
        # Visitar cada una de los parametros asociados

    def visit(self, n: ArgList, env: Symtab):
        # Visitar cada una de los argumentos asociados
