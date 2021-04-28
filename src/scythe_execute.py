from sly.yacc import _unique_names


class SExecute:
	def __init__(self, tree, names):
		self.names = names
		result = self.walkTree(tree)
		if result is not None and isinstance(result, int):
			print(result)
		if isinstance(result, str) and result[0] == '"':
			print(result)

	def walkTree(self, node):
		if isinstance(node, int):
			return node
		if isinstance(node, str):
			return node

		if node is None:
			return None

		if node[0] == 'program':
			if node[1] == None:
				self.walkTree(node[2])
			else:
				self.walkTree(node[1])
				self.walkTree(node[2])

		if node[0] == 'num':
			return node[1]

		if node[0] == 'string':
			return node[1]

		if node[0] == 'add':
			return self.walkTree(node[1]) + self.walkTree(node[2])
		elif node[0] == 'sub':
			return self.walkTree(node[1]) - self.walkTree(node[2])
		elif node[0] == 'times':
			return self.walkTree(node[1]) * self.walkTree(node[2])
		elif node[0] == 'div':
			return self.walkTree(node[1]) / self.walkTree(node[2])
		elif node[0] == 'greater':
			return self.walkTree(node[1]) > self.walkTree(node[2])
		elif node[0] == 'less':
			return self.walkTree(node[1]) < self.walkTree(node[2])
		elif node[0] == 'less_or_equal':
			return self.walkTree(node[1]) <= self.walkTree(node[2])

		if node[0] == 'var_assign':
			self.names[node[1]] = self.walkTree(node[2])
			return node[1]

		if node[0] == 'var':
			try:
				return self.names[node[1]]
			except LookupError:
				print("Undefined variable '"+node[1]+"' found!")

		if node[0] == 'syout':
			print(self.walkTree(node[1]))

		if node[0] == 'datatype':
			data = str(type(self.walkTree(node[1])))
			return data[data.find('\'') + 1: len(data) - 2]

		if node[0] == 'int_con':
			return int(self.walkTree(node[1]))
	
		if node[0] == 'str_con':
			return str(self.walkTree(node[1]))
		
		if node[0] == 'compare':
			if self.walkTree(node[1]):
				return self.walkTree(node[2])
			else:
				return self.walkTree(node[3])