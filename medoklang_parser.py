from sly import Parser
import medoklang_lexer

class sintaksis(Parser):
    tokens = medoklang_lexer.leksikal.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.env = {}

    @_('')
    def statement(self, p):
        pass

    # Implementasi tabel informasi untuk statement FOR
    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    # Implementasi tabel informasi untuk statement IF
    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    # Implementasi tabel informasi untuk statement FUN
    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    # Implementasi tabel informasi untuk statement FUN_CALL
    @_('NAME "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    # Implementasi tabel informasi untuk condition EQEQ
    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    # Implementasi tabel informasi untuk var_assign
    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        self.env[p.NAME] = self.walkTree(p.expr)  # Menyimpan nilai ekspresi ke dalam tabel informasi
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        self.env[p.NAME] = p.STRING  # Menyimpan nilai string ke dalam tabel informasi
        return ('var_assign', p.NAME, p.STRING)

    # Implementasi tabel informasi untuk ekspresi
    @_('expr')
    def statement(self, p):
        return p.expr

    # Implementasi tabel informasi untuk operasi matematika
    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    # Implementasi tabel informasi untuk variabel
    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    # Implementasi tabel informasi untuk angka
    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)

    # Implementasi tabel informasi untuk statement PRINT
    @_('PRINT expr')
    def expr(self, p):
        return ('print', p.expr)

    @_('PRINT STRING')
    def statement(self, p):
        return ('print', p.STRING)

if __name__ == '__main__':
    lexer = medoklang_lexer.leksikal()
    parser = sintaksis()
    env = {}

    while True:
        try:
            text = input('medok > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
