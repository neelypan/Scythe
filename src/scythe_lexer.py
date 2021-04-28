from sly import Lexer


class SLexer(Lexer):
    tokens = {ID, NUMBER, STRING, SYOUT, SYIN,
              DATATYPE, STR, INT, IF, ELSE, COMMENT, LESS_OR_EQUAL, GREATER_OR_EQUAL}
    ignore = '\r \t'
    literals = {'=', '+', '-', '*', '/',
                '(', ')', '<', '>', '<=', '>=', '{', '}'}

    # Tokens
    COMMENT = r'\//.*'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['syout'] = SYOUT
    ID['syin'] = SYIN
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
