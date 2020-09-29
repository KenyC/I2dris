from idr_parse import Expr, Type

class Pos:
	"""docstring for Pos"""
	def __init__(self, line_init, line_end, pos_init, pos_end):
		super(Pos, self).__init__()
		self.line_init = line_init
		self.line_end = line_end
		self.pos_init = pos_init
		self.pos_end = pos_end


	def interpret(positions):
		if any(pos.type != Type.Expr or len(pos.obj) != 2 for pos in positions):
			return None

		if any(coord.type != Type.Int for pos in positions for coord in pos.obj):
			return None

		return Pos(*(coord.obj for pos in positions for coord in pos.obj))

	def __str__(self):
		return "[{line_init}:{pos_init}-{line_end}:{pos_end}]".format(
			line_init = self.line_init,
			line_end  = self.line_end,
			pos_init  = self.pos_init,
			pos_end   = self.pos_end
		)


		

class Warning:
	"""docstring for Warning"""
	def __init__(self, file, pos, error):
		super(Warning, self).__init__()
		self.file  = file
		self.pos   = pos
		self.error = error


	def interpret(args):
		if args.type != Type.Expr or len(args.obj) != 4:
			return None
		
		if args.obj[0].type != Type.String or args.obj[3] != Type.String:
			return None 

		pos = Pos.interpret(*args[1:3])
		if pos is None:
			return None

		return Warning(expr.obj[1].obj)

	def __str__(self):
		return "Error ({file}{pos}) {error}".format(
			file  = self.file,
			pos   = self.pos,
			error = self.error
		)


class WriteString:
	"""docstring for WriteString"""
	def __init__(self, to_write):
		super(WriteString, self).__init__()
		self.to_write = to_write
		

	def interpret(arg):
		if arg.type != Type.String:
			return None
		return WriteString(arg.obj)

	def __str__(self):
		return "Write " + self.to_write

class Return:
	"""docstring for WriteString"""
	def __init__(self, status, message = None):
		super(Return, self).__init__()
		self.status  = status
		self.message = message
		

	def interpret(arg):
		if arg.type != Type.Expr:
			return None

		if len(arg.obj) < 2:
			return None

		if arg.obj[0].type != Type.Symbol:
			return None 

		message = arg.obj[1]
		symbol  = arg.obj[0].obj

		if   message.type == Type.Expr:
			return Return(symbol)
		elif message.type == Type.String:
			return Return(symbol, message.obj)

	def __str__(self):
		return "Return {status}: {message}".format(
			status  = self.status,
			message = self.message
		)
		

legible_commands = {
	"warning"       : Warning.interpret,
	"write-string"  : WriteString.interpret,
	"return"        : Return.interpret
}
def interpret(expr):
	if expr.type != Type.Expr:
		return None
	
	if len(expr.obj) != 3:
		return None

	if expr.obj[0].type != Type.Symbol:
		return None

	symbol = expr.obj[0].obj
	arg    = expr.obj[1]
	if symbol in legible_commands:
		return legible_commands[symbol](arg)

