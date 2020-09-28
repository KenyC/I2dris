import enum

class Type(enum.Enum):
	String = 1
	Int    = 2
	Symbol = 3
	Expr   = 4



class Expr:
	"""Expression"""
	def __init__(self, enum, obj):
		self.obj  = obj
		self.type = enum

	def __str__(self):
		if   self.type == Type.String:
			return self.obj
		elif self.type == Type.Symbol:
			return ":" + self.obj
		elif self.type == Type.Int:
			return str(self.obj)
		elif self.type == Type.Expr:
			return "({})".format(
				" ".join(
					[str(child) for child in self.obj]
				)
			)
	def __repr__(self):
		return "Expr({type}, {obj})".format(
			type  = self.type,
			obj   = self.obj
		)		



		


def unpack_string(string):
	return string[0], string[1:]

def parse_char(char, string):
	if string:
		c, rest = unpack_string(string)

		if c != char:
			return None, string	
		else:
			return char, rest
	else:
		return None, string

def parse_string(string):
	if string:
		c, rest = unpack_string(string)

		if c == '"':
			to_return = ""
			c, rest = unpack_string(rest)

			while c != '"':
				if c == "\\":
					c1, rest = unpack_string(rest)
					if c1 in '"\\':
						to_return += c1
					else:
						to_return += c
						rest = c1 + rest
				else:
					to_return += c

				c, rest = unpack_string(rest)

			return Expr(Type.String, to_return), rest
		else:
			return None, string
	else:
		return None, string

numbers = "0123456789"
def parse_int(string):
	if string:
		to_return = ""
		c, rest = unpack_string(string)

		while c in numbers:
			to_return += c
			if rest:
				c, rest = unpack_string(rest)
			else:
				c = ""
				break
		
		if to_return:
			return (Expr(Type.Int, int(to_return)), c + rest)
		else:
			return None, string
	else:
		return None, string

spaces = " \n\t\r)\""
def parse_symbol(string):
	if string:
		c, rest = unpack_string(string)
		if c != ":":
			return None, string

		to_return = ""

		while True:
			if rest:
				c, rest = unpack_string(rest)
				if c in spaces:
					return (Expr(Type.Symbol, to_return), c + rest)
				else:
					to_return += c
			else:
				return (Expr(Type.Symbol, to_return), "")

		return (Expr(Type.Symbol, to_return), rest)
	else:
		return None, string


def parse_expr(string):
	if string:
		
		result, rest = parse_char("(", string)
		if result is None:
			return result, rest

		to_return = []

		parsers = (parse_symbol, parse_int, parse_string, parse_expr)

		while True:
			foundit = False
			for parser in parsers:
				result, rest = parser(rest)
				if result is not None:
					foundit = True
					to_return.append(result)
					break

			if foundit:
				result, rest = parse_char(" ", rest)
				if result is not None:
					continue
			else:
				break

		result, rest = parse_char(")", rest)
		if result is not None:
			return Expr(Type.Expr, to_return), rest
		else:
			return None, string

	else:
		return None, string



# def parse_expr(string):
# 	if string:
# 		pass
# 	else:
# 		pass