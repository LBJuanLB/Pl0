# interp.py
'''
Intérprete
==========

Este es un intérprete que puede ejecutar programas `PL0`  directamente desde el código IR generado. Esto se puede utilizar para comprobar los resultados sin necesidad de una dependencia de LLVM.

Para ejecutar un programa utilice:

    bash % python3 -m pl0.interp someprogram.pl0

'''
import sys

class Interpreter(object):
  '''
  Ejecuta un intérprete en el código intermedio SSA generado para su compilador. La idea de implementación es la siguiente. Dada una secuencia de tuplas de instrucciones como:

    code = [
      ('MOVI', 1, 'R1'),
      ('MOVI', 2, 'R2'),
      ('ADDI', 'R1', 'R2', 'R3'),
      ('PRINTI', 'R3')
      ...
    ]

  La clase ejecuta métodos self.run_opcode(args). Por ejemplo:

     self.run_MOVI(1, 'R1')
     self.run_MOVI(2, 'R2')
     self.run_ADDI('R1','R2','R3')
     self.run_PRINTI('R3')
  '''
  def __init__(self):
    # Variable storage
    self.vars = { }

    # Registers
    self.registers = { }

  def execute(self, code):
    for inst, *args in code:
      getattr(self, f'run_{inst}')(*args)

  # Interpreter opcodes
  def run_MOVI(self, value, target):
    self.registers[target] = value
  run_MOVF = run_MOVI
  run_MOVB = run_MOVI

  def run_ADDI(self, left, right, target):
    self.registers[target] = self.registers[left] + self.registers[right]
  run_ADDF = run_ADDI

  def run_SUBI(self, left, right, target):
    self.registers[target] = self.registers[left] - self.registers[right]
  run_SUBF = run_SUBI

  def run_MULI(self, left, right, target):
    self.registers[target] = self.registers[left] * self.registers[right]
  run_MULF = run_MULI

  def run_DIVI(self, left, right, target):
    self.registers[target] = self.registers[left] // self.registers[right]

  def run_DIVF(self, left, right, target):
    self.registers[target] = self.registers[left] / self.registers[right]

  def run_PRINTI(self, value):
    print(self.registers[value])
  run_PRINTF = run_PRINTI

  def run_PRINTB(self, value):
    print(chr(self.registers[value]),end='')
    sys.stdout.flush()

  def run_VARI(self, name):
    self.vars[name] = 0

  def run_VARF(self, name):
    self.vars[name] = 0.0

  run_VARB = run_VARI

  def run_LOADI(self, name, target):
    self.registers[target] = self.vars[name]
  run_LOADF = run_LOADI
  run_LOADB = run_LOADI

  def run_STOREI(self, target, name):
    self.vars[name] = self.registers[target]
  run_STOREF = run_STOREI
  run_STOREB = run_STOREI
  
  def run_LABEL(self, name):
    pass