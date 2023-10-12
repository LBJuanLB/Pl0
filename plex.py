'''
pl0lex

Analizador Lexico para el lenguaje PL0
'''
import sly
from rich.console import  Console
from rich.table import Table

# Crea la tabla
table = Table(title='Análisis Léxico')
table.add_column('type')
table.add_column('value')
table.add_column('linea', justify='right')
table.add_column('index', justify='right')
table.add_column('end', justify='right')

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

    literals = '+-*/()[],.;:<>"'
    ignore = ' \t'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'(/\*(.|\n)*?\*/)')
    def ignore_comment(self,t):
        self.lineno += t.value.count('\n')
    
    @_(r'/\*(.|\n)+')
    def ignore_untermcomment(self,t):
        print(f"Line {self.lineno}. Unterminated comment.")
        self.lineno += t.value.count('\n')

    @_(r'[0]\d+.*')
    def numbers_error(self,t):
        print(f"Line {self.lineno}. Numero mal escrito {t.value}")
        self.lineno += t.value.count('\n')

    @_(r'(\+|-)?([0]|[1-9][0-9]*)(\.[0-9]+((e|E)(\+|-)?[0-9]+)?|(e|E)(\+|-)?[0-9]+)')
    def FLOAT(self,t):
        t.value = float(t.value)
        return t

    @_(r'((\+|-)?[1-9][0-9]*)|[0]')
    def INT(self,t):
        t.value = int(t.value)
        return t

    @_(r'".*\\e.*"')
    def error_escape(self,t):
        print(f"Line {self.lineno}. Caracter de escape ilegal en {t.value}")
        self.lineno += t.value.count('\n')

    @_(r'".*[^(\\|\n)]"')
    def LITERAL(self,t):
        length=len(t.value)
        i=0
        sentence=0
        cadena="\""
        while (i<length):
            if t.value[i] == "\"" and t.value[i-1] != "\\" and sentence==0:
                sentence=1
            elif t.value[i] == "\"" and t.value[i-1] != "\\" and sentence == 1:
                sentence=0
            elif sentence==1:
                cadena=cadena+t.value[i]
            i+=1
        t.value=cadena+"\""
        return t



    @_(r'".*\n')
    def ignore_unterstring(self,t):
        print(f"Line {self.lineno}. Unterminated string.")
        self.lineno += t.value.count('\n')

    @_(r'\d+[a-zA-Z_]+')
    def identifier_error(self,t):
        print(f"Line {self.lineno}. Nombre de la funcion o variable mal escrito {t.value}")
        self.lineno += t.value.count('\n')
    
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
    NAME = r'[a-zA-Z_]+[0-9-a-zA-Z_]*'
        
    def error(self, t):
            print(f"Line {self.lineno}. Caracter ilegal '{t.value[0]}'")
            self.index += 1

def main(argv):
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} filename")
        exit(1)
    
    lex = Lexer()
    txt = open(argv[1]).read()
    ##
    for tok in lex.tokenize(txt):
        #value=tok.value if isinstance(tok.value , str(tok.value))
        if isinstance(tok.value, str):
            value = tok.value
        else:
            value = tok.value
        table.add_row(tok.type,
                      str(value),
                      str(tok.lineno),
                      str(tok.index),
                      str(tok.end))
    console = Console()
    console.print(table)
        #print(tok)


if __name__ == '__main__':
    from sys import argv
    main(argv)