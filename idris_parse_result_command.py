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
		self.enum = enum
		


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
			return (Expr(int(to_return), Type.Int), c + rest)
		else:
			return None, string
	else:
		return None, string

spaces = " \n\t\r"
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
					return (to_return, c + rest)
				else:
					to_return += c
			else:
				return (to_return, "")

		return (Expr(to_return, Type.Symbol), rest)
	else:
		return None, string


def parse_expr(string):
	if string:
		
		result, rest = parse_char("(", string)
		if result is None:
			return result, rest

		to_return = []

		while True:
			result, rest = parse_symbol(rest)
			if result is not None:
				to_return.append(result)

				result, rest = parse_char(")", rest)
				if result is not None:
					break

				result, rest = parse_char(" ", rest)
				if result is not None:
					continue
				else:
					return None, string


			result, rest = parse_int(rest)
			if result is not None:
				to_return.append(result)

				result, rest = parse_char(")", rest)
				if result is not None:
					break

				result, rest = parse_char(" ", rest)
				if result is not None:
					continue
				else:
					return None, string


			result, rest = parse_string(rest)
			if result is not None:
				to_return.append(result)

				result, rest = parse_char(")", rest)
				if result is not None:
					break

				result, rest = parse_char(" ", rest)
				if result is not None:
					continue
				else:
					return None, string

			result, rest = parse_expr(rest)
			if result is not None:
				to_return.append(result)

				result, rest = parse_char(")", rest)
				if result is not None:
					break

				result, rest = parse_char(" ", rest)
				if result is not None:
					continue
				else:
					return None, string

			return None, string

		return Expr(to_return, Type.Expr), rest

	else:
		return None, string



# def parse_expr(string):
# 	if string:
# 		pass
# 	else:
# 		pass