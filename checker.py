from arbol import *


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

	def visit(self, n: Literal, env: Symtab):
		# Devolver datatype

	def visit(self, n: Location, env: Symtab):
		# Buscar en Symtab y extraer datatype (No se encuentra?)
		# Devuelvo el datatype

	def visit(self, n: TypeCast, env: Symtab):
		# Visitar la expresion asociada
		# Devolver datatype asociado al nodo

	def visit(self, n: Assign, env: Symtab):
		# Visitar el hijo izquierdo (devuelve datatype)
		# Visitar el hijo derecho (devuelve datatype)
		# Comparar ambos tipo de datatype

	def visit(self, n: FuncCall, env: Symtab):
		# Buscar la funcion en Symtab (extraer: Tipo de retorno, el # de parametros)
		# Visitar la lista de Argumentos
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

	def visit(self, n: FuncDefinition, env: Symtab):
		# Agregar el nombre de la funcion a Symtab
		# Crear un nuevo contexto (Symtab)
		# Visitar ParamList, VarList, StmtList
		# Determinar el datatype de la funcion (revisando instrucciones return)

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

	def visit(self, n: Program, env: Symtab):
		# Crear un nuevo contexto (Symtab global)
		# Visitar cada una de las declaraciones asociadas

	def visit(self, n: StmtList, env: Symtab):
		# Visitar cada una de las instruciones asociadas

	def visit(self, n: VarList, env: Symtab):
		# Visitar cada una de las variables asociadas

	def visit(self, n: ParmList, env: Symtab):
		# Visitar cada una de los parametros asociados

	def visit(self, n: ArgList, env: Symtab):
		# Visitar cada una de los argumentos asociados
