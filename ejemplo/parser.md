# Analizador Sintáctico

En esta parte del proyecto, se construirá un módulo de análisis
sintático para **PL0**. Para ello, se basará en su módulo de
análisis léxico y en el uso de una herramienta adicional de
generación de código de forma automática llamada `sly.Parser`
(un derivado de `bison` en Python--la popular herramienta 
GNU LALR(1) de generadores sintáticos).

## Introducción

La mayoría de los compiladores modernos se construyen con la ayuda de
herramientas que generan análisis sintáctico automáticamente e
intentan crear el código del analizador a partir de las reglas en BNF.
Este enfoque es particulamente apropiado para la construcción de compiladores,
ya que muchos de los algoritmos de análisis sintático mas comunes son guiados
por tablas. Además, la construcción de estas tablas es muy tediosa,
difícil y propensa a errores si se intenta hacerlo a mano.

Una de las herramientas más populares para la de construcción de
compiladores es referida a menudo como `yacc` (Yet Another Compiler Compiler).
El nombre en sí es un poco engañoso, ya que hay literalmente docenas
de versiones de herramientas `yacc` disponibles para diferentes plataformas,
diferentes lenguajes de implementación, y diferentes algoritmos de análisis
sintáctico. En los sistemas Unix, `yacc` es una utilidad estándar
que puede ser utilizada para construir los analizadores en *C/C++*. La versión
GNU de `yacc` es conocida como `bison`. Una versión de Berkeley conocida como
`byacc` también está disponible en muchas plataformas.

La mayoría de herramientas basadas en `yacc` cuentan con alguna forma de análisis
LR---tipicamente LALR(1). Cada vez que alguien se refiere a un analizador generado por `yacc`,
significa que se han utilizado alguna variante de estas herramientas. Además, a menos
que se indique lo contrario, usualmente implica que el analizador esta usando análisis LR.

Para este proyecto, se utilizará una herramienta como yacc para Python para
crear el analizador de **PL0**. Como resultado, el analizador va a crear un árbol
de sintáxis abstracta (AST), del programa de entrada. Además, el analizador
tendrá que informar diversos tipos de errores de sintáxis que aparezcan
en el archivo de entrada.

## Parte 1 - Corregir el Proyecto 1

Modifique su analizador léxico para corregir todas las pruebas que hayan fallado
en el Proyecto 1. Recuperarán la mitad de los puntos perdidos en el Proyecto 1 al
pasar las pruebas cuando se entregue el Proyecto 2.

## Parte 2 - Analizador Sintáctico de PL0

`sly.Parser` es la herramienta del compilador yacc para Python que se utilizará para
construir el analizador sintáctico.

Cree un archivo llamado 'pparse.py' que contenga las definiciones del analizador
sintático para el lenguaje. Este archivo contendrá una colección
de funciones de Python correspondientes a las reglas de la gramática que se
definieron en el Proyecto 1.


La mejor forma de describir el contenido del archivo del analizador es ver un ejemplo.
El ejemplo está en ~/basic64/basparse.py tiene una implementación completa de un 
analizador sintáctico para el lenguaje BASIC Darmounth 64. El archivo 'basparse.py' 
tiene comentarios describiendo el sistema y puede ser usado como una plantilla para 
su analizador sintáctico.

Para probar su analizador, simplemente corralo con un archivo de pruebas.  Por ejemplo:

<blockquote>
<pre>% python pparse.py hello.pl0
</pre>
</blockquote>

La salida principal de su analizador debe ser una lista de errores sintácticos
(si los hay). Estos se usarán como bases para la mayoría de nuestras pruebas.
Además, se deberá incluir código para imprimir el árbol del
análisis. Por ejemplo, su código puede producir una salida similar a esto:

<blockquote>
<pre>% python pparse.py hello.pl0
:::: Parse Tree ::::
program
  +-- funclist
        +-- function (main)
              |-- parmlist
              |-- varlist
              |     |-- variable
              |     |     +-- parm (x)
              |     |           +-- type_int
              |     +-- variable
              |           +-- parm (y)
              |                 +-- type_int
              +-- statements
                    |-- print ("Hello World\n")
                    |-- read
                    |     +-- loc_id (x)
                    |-- assign
                    |     |-- loc_id (y)
                    |     +-- expr_binary (*)
                    |           |-- expr_int (3)
                    |           +-- expr_id (x)
                    +-- write
                          +-- expr_id (y)
</pre>
</blockquote>

Tenga en cuenta que la estructura del árbol de su analizador dependerá de
como usted escribió las reglas y el nombre que se haya decidido usar en el AST
(no necesita coincidir con el ejemplo anterior).

Para probar el analizador, se deberá correr con una gran variedad de archivos de
entrada para ver si produce la salida esperada.  En este caso, la salida deberá
ser solamente un mensaje de error (o nada) producido por su analizador léxico o
sintáctico.

Documentación detallada acerca de 'sly.Parser' puede ser leida desde su archivo fuente
o mirando la documentación que hay en la página web.
Si usted ha tenido experiencia previa con yacc o bison, la mayoría de conceptos
asociados con el uso de estas herramientas han sido trasladados directamente para ser
usados en sly.Parser.

## Procedimiento de entrega

1. Su analizador deberá estar contenido en un archivo 'pparse.py'.   Debemos ser
capaces de correr este archivo de la siguiente manera para realizar una prueba:

<pre>% python pparse.py testname.pl0
</pre>

Además, debemos ser capaces de correr las anteriores pruebas léxicas para el
proyecto 1. Por ejemplo:

<pre>% python plex.py testname.pl0
</pre>

2. Asegurarse de tener un archivo README que incluya sus nombres y cualquier cosa notable
acerca de su implementación.

3. Cree un archivo tar de Unix para su proyecto.  Este archivo tar deberá contener el
directorio 'pl0' y debe de estar basado en el nombre de su usuario de correo. Por ejemplo:

<pre>% tar -cf <em>sulogin</em>.tar pl0
</pre>

4. Suba este archivo a *classroom* de la clase.

5. Tareas de última hora no son aceptadas. No se recibirá ningún trabajo después
de la fecha límite.
