'''
pl0lex

Analizador Lexico para el lenguaje PL0
'''
import sly

class Lexer(sly.Lexer):
    tokens = {
        #Palabras Reservadas
        FUN, BEGIN, END, WHILE, DO, IF, THEN, ELSE,
        PRINT, WRITE, READ, RETURN, SKIP, BREAK, INT_T,
        FLOAT_T,
        #Asignacion (:=)
        ASIG, 

        #Operadores de Relacion (MEI = Menor igual <=) (MAI = Mayor igual >=) (II = Igual igual ==) (DI = Diferente igual !=)
        AND, OR, NOT, MEI, MAI, II, DI,

        #Literales
        INT, FLOAT, NAME, LITERAL,
    }
    literals = '+-*/()[],;:<>"'

    ignore = ' \t\r\n'

    @_(r'-?([0]|[1-9][0-9]*)\,[0-9]+((e|E)(\+|-)[0-9]+)?')
    def FLOAT(self,t):
        t.value = float(t.value)
        return t

    @_(r'(-?[1-9][0-9]*)|[0]')
    def INT(self,t):
        t.value = int(t.value)
        return t
    
    
    LITERAL = r'"([^"]*)"'
    MEI    =r'<='
    MAI    =r'>='
    II     =r'=='
    DI     =r'!='
    WHILE = r'[Ww][Hh][Ii][Ll][Ee]\b'
    ASIG   =r':='
    NOT    =r'[Nn][oO][Tt]\b'
    FUN    = r'[Ff][uU][Nn]\b'
    READ   = r'[rR][eE][aA][dD]\b' 
    WRITE   = r'[wW][rR][iI][Tt][eE]\b'
    PRINT  = r'[Pp][Rr][Ii][Nn][Tt]\b'
    DO   = r'[Dd][Oo]\b'
    IF     = r'[iI][fF]\b'
    THEN   = r'[Tt][Hh][Ee][Nn]\b'
    ELSE =r'[Ee][Ll][Ss][Ee]\b'
    END    = r'[Ee][Nn][Dd]\b'
    BREAK  = r'[Bb][Rr][Ee][Aa][Kk]\b'
    RETURN = r'[Rr][Ee][Tt][uU][rR][nN]\b'
    SKIP= r'[sS][Kk][iI][pP]\b'
    BEGIN    = r'[Bb][Ee][Gg][Ii][Nn]\b'
    AND    = r'[Aa][Nn][Dd]\b'
    OR    = r'[Oo][Rr]\b'
    FLOAT_T  = r'[Ff][Ll][Oo][Aa][Tt]\b'
    INT_T = r'[iI][Nn][tT]\b'
    
    NAME = r'[a-zA-Z]+[0-9]*[a-zA-Z]*'
def error(self, t):
        print(f"Caracter ilegal '{t.value[0]}'")
        self.index += 1

def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)
    
    lex = Lexer()
    txt = open(argv[1]).read()

    for tok in lex.tokenize(txt):
        print(tok)


if __name__ == '__main__':
    from sys import argv
    main(argv)

set
#probando