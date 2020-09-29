"""
Shallow Idris Parse to determine declarations from commands or expressions
"""

import enum
import re

class CodeType(enum.IntEnum):
	Declaration = 0
	Expression  = 1
	REPL_Cmd    = 2
	Undeclare   = 3

decl_regex = re.compile(r"^(\n|\s)*([a-zA-Z][a-zA-Z0-9_]*)\s((:)|(.*=))")
white_spaces = " \n\t\r"
def parse_code_into_codetypes(code):
	"""
	Split code into lines which are definitions, lines which are commands, lines which are expressions

	Rules used are as follows:
		1) Lines which start with ":" are REPL commmands
		2) Lines which contain " : " or " = " are declaratations
		3) Unindented lines which do not contain "=" or ":" are expressions
		4) All other lines are declarations
	"""
	stack_definitions = []
	to_return         = []

	def add_stack_to_return():
		if stack_definitions and any(map(str.strip, stack_definitions)):
			# find names defined 
			to_undeclare = set()
			for line in stack_definitions:
				match = decl_regex.match(line)
				if match:
					identifier = match.group(2)

					if identifier not in to_undeclare:
						to_undeclare.add(identifier)
						to_return.append((
							CodeType.Undeclare,
							identifier
						))


			to_return.append((
				CodeType.Declaration, 
				"\n".join(stack_definitions)
			))

	for line in code.splitlines():
		if not line:
			stack_definitions.append(line) # Adding empty lines in case line numbering one day becomes relevant
		elif line[0] == ":":
			add_stack_to_return()
			to_return.append((CodeType.REPL_Cmd, line))
		elif " : " in line or " = " in line or not line:
			stack_definitions.append(line)
		elif line[0] not in white_spaces:
			add_stack_to_return()
			to_return.append((CodeType.Expression, line))
		else:
			stack_definitions.append(line)

	add_stack_to_return()
	return to_return


if __name__ == "__main__":
	test_code = """
a = 5
2+3
a : Bool
a = True
:l file
1+1
	"""
	test_code2 = """
add : Int'' -> Int'' -> Int''
add n m a f = (n a f) . (m a f)

prod : Int'' -> Int'' -> Int''
prod n m a = (n a) . (m a)

exponent : Int'' -> Int'' -> Int''
exponent m n a = n (a -> a)  $ m a
	"""
