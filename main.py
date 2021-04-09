from sly import Lexer, Parser

class SLexer(Lexer):
	tokens = {ID, NUMBER}
	ignore = '\r \t'

	ignore_comment = r'\//.*'
	# ignore_newline = r'\n+'
	literals = {'=', '+', '-', '*', '/', '(', ')'}

	# Tokens
	ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

	@_(r'\d+')
	def NUMBER(self, t):
		t.value = int(t.value)
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

	@_('ID "=" expr')
	def statement(self, p):
		self.names[p.ID] = p.expr

	@_('expr')
	def statement(self, p):
		print(p.expr)

	@_('expr "+" expr')
	def expr(self, p):
		return p.expr0 + p.expr1

	@_('expr "-" expr')
	def expr(self, p):
		return p.expr0 - p.expr1

	@_('expr "*" expr')
	def expr(self, p):
		return p.expr0 * p.expr1

	@_('expr "/" expr')
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

	@_('ID')
	def expr(self, p):
		try:
			return self.names[p.ID]
		except LookupError:
			print(f'Undefined name {p.ID}')
			return 0


if __name__ == '__main__':
	lexer = SLexer()
	parser = SParser()

	data = open('main.scy', 'r')
	lines = data.readlines()
	for i in lines:
		if i:
			parser.parse(lexer.tokenize(i))


