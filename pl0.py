# pl0.py
'''
usage: pl0.py [-h] [-d] [-o OUT] [-l] [-D] [-p] [-I] [--sym] [-S] [-R] input

Compiler for PL0

positional arguments:
  input              PL0 program file to compile

optional arguments:
  -h, --help         show this help message and exit
  -D, --debug        Generate assembly with extra information (for debugging purposes)
  -o OUT, --out OUT  File name to store generated executable
  -l, --lex          Store output of lexer
  -d, --dot          Generate AST graph as DOT format
  -p, --png          Generate AST graph as png format
  -pAST, --printAST  Print the AST
  -c, --check        Check the program for errors
  -I, --ir           Dump the generated Intermediate representation
  -RunI, --runir     Run the generated Intermediate representation
  --sym              Dump the symbol table
  -S, --asm          Store the generated assembly file
  -R, --exec         Execute the generated program
'''
from contextlib import redirect_stdout
#from rich       import print
from plex       import print_lexer
from pparse     import gen_ast, print_ast
from context    import Context
from checker   import Checker
from instrucciones import AST
from interp    import Interpreter

import argparse


def parse_args():
  cli = argparse.ArgumentParser(
    prog='pl0.py',
    description='Compiler for PL0 programs')

  cli.add_argument(
    '-v', '--version',
    action='version',
    version='0.1')

  fgroup = cli.add_argument_group('Formatting options')

  fgroup.add_argument(
    'input',
    type=str,
    nargs='?',
    help='PL0 program file to compile')

  mutex = fgroup.add_mutually_exclusive_group()

  mutex.add_argument(
    '-l', '--lex',
    action='store_true',
    default=False,
    help='Store output of lexer')

  mutex.add_argument(
    '-d', '--dot',
    action='store_true',
    default=False,
    help='Generate AST graph as DOT format')

  mutex.add_argument(
    '-p', '--png',
    action='store_true',
    help='Generate AST graph as png format')
  
  mutex.add_argument(
    '-c', '--check',
    action='store_true',
    help='Check the program for errors')  

  mutex.add_argument(
    '--sym',
    action='store_true',
    help='Dump the symbol table')
  
  mutex.add_argument(
    '-I', '--ir',
    action='store_true',
    help='Dump the generated Intermediate representation')
  
  mutex.add_argument(
    '-RunI', '--runir',
    action='store_true',
    help='Run the generated Intermediate representation')
  
  mutex.add_argument(
    '-pAST', '--printAST',
    action='store_true',
    help='Print the AST')

  return cli.parse_args()


if __name__ == '__main__':

  args = parse_args()
  context = Context()

  if args.input: fname = args.input

  with open(fname, encoding='utf-8') as file:
    source = file.read()

  if args.lex:
    flex = fname.split('.')[0] + '.lex'
    print(f'print lexer: {flex}')
    with open(flex, 'w', encoding='utf-8') as f:
      with redirect_stdout(f):
        print_lexer(source)

  elif args.dot or args.png:
    '''Primero hacemos el checker para ver si hay errores, si no hay errores entonces generamos el AST y el dot'''
    context.parse(source)
    checker = Checker(context)
    checker.checker(context.ast,context)
    if context.have_errors:
      exit(1)
    
    ast, dot = gen_ast(source)
    base = fname.split('.')[0]
    if args.dot:
      fdot = base + '.dot'
      print(f'print ast: {fdot}')
      with open(fdot, 'w') as f:
        with redirect_stdout(f):
          print(dot)

    elif args.png:
      ...

    else:
      context.parse(source)
      context.run()
  
  elif args.check:
    context.parse(source)
    checker = Checker(context)
    checker.checker(context.ast,context)
    if context.have_errors == False:
      print("No hay errores!")

  elif args.sym:
    context.parse(source)
    checker = Checker(context)
    checker.symtab=checker.checker(context.ast,context)
    if context.have_errors == False:
      flex = fname.split('.')[0] + '.sym'
      print(f'print symbol table: {flex}')
      with open(flex, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):
          checker.symtab.print_symbol_table()
    else:
      print("Hay errores en el programa, no se puede generar la tabla de simbolos")
    
  elif args.ir:
    context.parse(source)
    checker = Checker(context)
    tabla=checker.checker(context.ast,context)
    if context.have_errors == False:
      ircode = AST()
      flex = fname.split('.')[0] + '.ir'
      print(f'print intermediate representation: {flex}')
      with open(flex, 'w', encoding='utf-8') as f:
        with redirect_stdout(f):
          inst=ircode.instrucciones(context.ast)
          for i in inst:
            print(str(i)+",")
    else:
      print("Hay errores en el programa, no se puede generar el codigo intermedio")
      
  elif args.runir:
    context.parse(source)
    checker = Checker(context)
    tabla=checker.checker(context.ast,context)
    if context.have_errors == False:
      ircode = AST()
      inst=ircode.instrucciones(context.ast)
      interpreter = Interpreter()
      interpreter.execute(inst)
    else:
      print("Hay errores en el programa, no se puede generar el codigo intermedio")
      
  elif args.printAST:
    from rich import print
    context.parse(source)
    print(context.ast)

  else:

    try:
      while True:
        source = input('pl0 $ ')
        context.parse(source)
        if not context.have_errors:
          for stmt in context.ast.funlist:
            context.ast = stmt
            context.run()

    except EOFError:
      pass

