from sly import Lexer

class leksikal(Lexer):
    tokens = { PRINT, NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ }
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';' }

    PRINT = r'cetak'
    IF = r'nek'
    THEN = r'mongko'
    ELSE = r'liyane'
    FOR = r'nggo'
    TO = r'nganti'
    FUN = r'fungsi'
    ARROW = r'-->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'"[^"]*"'

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')

    def error(self, t):
        raise ValueError(f"Karakter ilegal '{t.value[0]}' di indeks {t.index}")


if __name__ == '__main__':
    lexer = leksikal()
    env = {}
    while True:
        try:
            text = input('medok > ')
        except EOFError:
            break
        if text:
            try:
                lex = lexer.tokenize(text)
                for token in lex:
                    print(token)
            except Exception as e:
                print("Ana kesalahan:", str(e))
