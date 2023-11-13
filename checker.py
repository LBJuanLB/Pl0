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
    def __init__(self):
        self.whileBool=False
        self.error=False
        self.funcall=False
    @classmethod
    def checker(cls, n:node):
        c=cls()
        return n.accept(c, Symtab())
        
    def visit(self, n: Program, env: Symtab):
        # Crear un nuevo contexto (Symtab global)
        
        Table = Symtab()
        # Visitar cada una de las declaraciones asociadas
        for funt in n.funlist:
            funt.accept(self, Table)
        return self.error

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
        datatype=None  
        if n.statements != None:
            
            for stmt in n.statements:
                stmt.accept(self, Table)
                 # Determinar el datatype de la funcion (revisando instrucciones return)
                if isinstance(stmt, Return):
                    datatype=stmt.datatype
                    n.datatype=datatype
            
        return datatype

    def visit(self, n: Name, env: Symtab):
        # Buscar el nombre en Symtab
        nombre=env.get(n.name)
        if nombre == None:
            print(f'No se encuentra {n.name}')
            self.error=True

    def visit(self, n: Literal, env: Symtab):
        # Devolver datatype
        return n.datatype.name
    
    def visit(self, n: Location, env: Symtab):
        # Buscar en Symtab y extraer datatype (No se encuentra?)
        node = env.get(n.name)
        if node == None:
            print(f'No se encuentra {n.name}')
            self.error=True
        elif isinstance(n, ArrayLocation):
            dattype=n.expr.accept(self, env)
            if dattype != 'int':
                print(f'El indice del array {n.name} no es un entero')
                self.error=True
            if isinstance(node.datatype, SimpleType) and self.funcall==False :
                print(f' {n.name} es una variable, no un array')
                self.error=True 
        elif isinstance(n, SimpleLocation) :
            if isinstance(node.datatype, ArrayType)and self.funcall==False:
                print(f' {n.name} es un array, no una variable')   
                self.error=True
          
        # Devuelvo el datatype
        return node.datatype.name

    def visit(self, n: TypeCast, env: Symtab):
        # Visitar la expresion asociada
        n.expr.accept(self, env)
        # Devolver datatype asociado al nodo
        return n.datatype
    

    def visit(self, n: FunCall, env: Symtab):
        self.funcall=True
        # Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
        node = env.get(n.name)
        #Tipo de retorno
        datatype=node.datatype
        #Num Parametros
        NumParm=len(node.arguments)   
        # Visitar la lista de Argumentos
        listdtype=[]
        listargument=[]
        listantype=[]
        if n.exprlist != None:
            for arg in n.exprlist:
                listdtype.append(arg.accept(self, env))
                if  isinstance(arg, SimpleLocation) or  isinstance(arg,ArrayLocation):
                    # Buscar la Variable en Symtab
                    nodo=env.get(arg.name)
                    if isinstance(nodo.datatype, ArrayType):
                        listargument.append(nodo.datatype.expr.value)
                    else:
                        listargument.append(None) 
                    listantype.append(arg)
                        

        if n.exprlist == None:
            print(f'Numero de argumentos incorrecto')
            self.error=True
        else:
            # Comparar el numero de argumentos con parametros
            if NumParm != len(n.exprlist):
                print(f'Numero de argumentos incorrecto')
                self.error=True
            else:
                # Comparar cada uno de los tipos de los argumentos con los parametros
                j=0
                for i in node.arguments:
                    if i.datatype.name != listdtype[j]:
                        print(f"El tipo de dato del para el parametro {i.name} es incorrecto. Tiene {listdtype[j]} y se esperaba {i.datatype.name}. En llamado de la funcion {n.name}")
                        self.error=True
                    if isinstance(i.datatype, ArrayType) :
                        if i.datatype.expr.value != listargument[j]:
                            if listargument[j] == None:
                                print(f"En el parametro  {i.name} no se le ingreso un tipo de dato array")
                            else:
                                print(f"El Tamaño del Array para el parametro  {i.name} es incorrecto. Envia un tamaño de {listargument[j]} y se esperaba {i.datatype.expr.value}. En llamado de la funcion {n.name}")
                            self.error=True
                        elif  isinstance(listantype[j], ArrayLocation):
                            print(f"El parametro {i.name} es un array. No le esta enviando un array")
                            self.error=True
                    elif isinstance(i.datatype, SimpleType) :
                        if listargument!=[]: 
                            if listargument[j] != None and isinstance(listantype[j], SimpleLocation):
                                print(f"El parametro {i.name} es una variable. No le esta enviando una variable")
                                self.error=True
                       
                    j+=1
                self.funcall=False
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
            print(f'No se puede operar {izq} con {der}')
            self.error=True
        else:
            n.datatype=SimpleType(datatype)
            return datatype

    def visit(self, n: Relation, env: Symtab):
        # Visitar el hijo izquierdo (devuelve datatype)
        izq=n.left.accept(self, env)
        # Visitar el hijo derecho (devuelve datatype)
        der=n.right.accept(self, env)
        # Comparar ambos tipo de datatype
        
        datatype=check_binary_op(n.op, izq, der)
        if datatype == None:
            print(f'No se puede operar {izq} con {der}')
            self.error=True
        else:
            n.datatype=datatype
            return datatype

    def visit(self, n: Unary, env: Symtab):
        # Visitar la expression asociada (devuelve datatype)
        data_type_expr=n.expr.accept(self, env)
        # Comparar datatype
        datatype=check_unary_op(n.op, data_type_expr)
        if datatype == None:
            print(f'No se puede operar {data_type_expr}')
            self.error=True
        else:
            n.datatype=datatype
            return datatype

    def visit(self, n: Argument, env: Symtab):
        # Agregar el nombre del parametro a Symtab
        env.add(n.name, n)
        return n.datatype

    def visit(self, n: Print, env: Symtab):
        ...     

    def visit(self, n: Write, env: Symtab):
        n.expr.accept(self, env)
        # Buscar la Variable en Symtab
        nodo=env.get(n.expr.name)
        if nodo == None:
            print(f'No se encuentra {n.expr.name}')
            self.error=True
        else:
            return nodo.datatype
    def visit(self, n: Read, env: Symtab):
        n.local.accept(self, env)
        # Buscar la Variable en Symtab
        nodo=env.get(n.local.name)
        if nodo == None:
            print(f'No se encuentra {n.local.name}')
            self.error=True
        else:
            return nodo.datatype.name

    def visit(self, n: While, env: Symtab):
        self.whileBool=True
        # Visitar la condicion del While (Comprobar tipo bool)
        condition_type = n.relation.accept(self, env)
        if condition_type != 'bool':
            print(f'Tipo incorrecto para la condición del While. Se esperaba "bool", pero se encontró "{condition_type}".')
            self.error=True
        # Visitar las Stmts
        n.statement.accept(self, env)
        self.whileBool=False

    def visit(self, n: Break, env: Symtab):
        # Esta dentro de un While?
        if self.whileBool == False:
            print('La instrucción "Break" debe estar dentro de un bucle "While".')
            self.error=True

    def visit(self, n: If, env: Symtab):
        # Visitar la condicion del IfStmt (Comprobar tipo bool)
        condition_type = n.relation.accept(self, env)
        if condition_type != 'bool':
            print(f'Tipo incorrecto para la condición del If. Se esperaba "bool", pero se encontró "{condition_type}".')
            self.error=True
        # Visitar las Stmts del then
        n.statement.accept(self, env)

        # Visitar las Stmts del else, si existen
        if n.if_else is not None:
            n.if_else.accept(self, env)
        

    def visit(self, n: Return, env: Symtab):
        # Visitar la expresion asociada
        padre=list(env.parent.entries.keys())
        nombre_funcion=padre[len(padre)-1] #Nombre de la funcion
        nodo_funcion=env.get(nombre_funcion)
        expr_type = n.expr.accept(self, env)
        # Actualizar el datatype de la funcion
        nodo_funcion.datatype=expr_type
        n.datatype = expr_type
        return expr_type
            

    def visit(self, n: Skip, env: Symtab):
        ...

    def visit(self, n: Begin, env: Symtab):
        # Visitar cada una de las instruciones asociadas
        for stmt in n.statements:
            stmt.accept(self, env)

    def visit(self, n: Assing, env:Symtab):
        # Buscar la Variable en Symtab
        nodo=env.get(n.location.name)
        
        #print (n.expr)
        #print(nodo)
        #print("------------------")
        if nodo == None:
            print(f'No se encuentra {n.location.name}')
            self.error=True
        else:
            # Visitar la expresion asociada
            expr_type = n.expr.accept(self, env)
            # Actualizar el datatype de la variable
            dataType= check_binary_op('+', nodo.datatype.name, expr_type)
            if dataType == None:
                print(f'No se puede asignar {expr_type} a {nodo.datatype.name}')
                self.error=True
            elif isinstance(nodo.datatype, ArrayType):
                if isinstance(n.location, SimpleLocation):
                    print(f'{n.location.name} es de tipo array, no se le puede asignar un valor a un array  ')
                    self.error=True
                elif isinstance(n.location, ArrayLocation):
                    if isinstance(n.location.expr, Unary):
                        if n.location.expr.op== '-':
                            print(f'El indice del array {n.location.name} no puede ser negativo  ')
                            self.error=True
                     
                
            else:
                return dataType
    


