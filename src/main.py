'''
Made by IMightBeMe and IMayBeMe on replit.com.

Source code is available on github at https://github.com/IMightBeMe/Scythe and replit at https://replit.com/@IMightBeMe/Scythe?v=1
'''

from sly import Lexer, Parser
import glob


class SLexer(Lexer):
    tokens = {ID, NUMBER, STRING, SYOUT, DATATYPE, STR, INT, IF, ELSE}
    ignore = '\r \t'
    ignore_comment = r'\//.*'
    literals = {'=', '+', '-', '*', '/', '(', ')', '<', '>', ';'}

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['syout'] = SYOUT
    ID['datatype'] = DATATYPE
    ID['str'] = STR
    ID['int'] = INT
    ID['if'] = IF
    ID['else'] = ELSE

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        lst = [char for char in t.value]
        del lst[0]
        del lst[len(lst) - 1]
        t.value = ''.join(lst)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'Illegal character {t.value[0]} on line {self.lineno}')
        self.index += 1


class SParser(Parser):
    tokens = SLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.names = {}

# still is being worked on please ignore the mess i made

    @_('IF condition ";" statement ";" ELSE ";" statement ";" ')
    def statement(self, p):
        # print(p.condition)
        # print(p.statement0)
        # print(p.statement1)
        pass

    @_('ID "=" expr')
    def statement(self, p):
        self.names[p.ID] = p.expr

    @_('print')
    def statement(self, p):
        print(p.print)

    @_('expr')
    def statement(self, p):
        pass

    @_('condition')
    def statement(self, p):
        pass

    @_('SYOUT "(" expr ")" ')
    def print(self, p):
        return p.expr

    @_('expr ">" expr')
    def condition(self, p):
        return p.expr0 > p.expr1

    @_('DATATYPE "(" expr ")" ')
    def expr(self, p):
        typ = str(type(p.expr))
        typ = typ.replace('<class ', '')
        typ = typ.replace('>', '')
        typ = typ.replace('\'', '')
        return typ

    @_('INT "(" expr ")" ')
    def expr(self, p):
        return int(p.expr)

    @_('STR "(" expr ")" ')
    def expr(self, p):
        print(p.expr)
        return str(p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        try:
            return p.expr0 + p.expr1
        except TypeError:
            return f'Unsupported data type \'+\' for {p.expr0} and {p.expr1}'

    @_('expr "-" expr ')
    def expr(self, p):
        try:
            return p.expr0 - p.expr1
        except TypeError:
            return f'Unsupported data type \'-\' for {p.expr0} and {p.expr1}'

    @_('expr "*" expr ')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr ')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('ID')
    def expr(self, p):
        try:
            return self.names[p.ID]
        except LookupError:
            return f'Undefined name {p.ID} '

if __name__ == '__main__':
    lexer = SLexer()
    parser = SParser()

    scythe_file = open('src/main.scy', 'r')

    lines = scythe_file.readlines()
    for i in lines:
        if i:
            parser.parse(lexer.tokenize(i))
