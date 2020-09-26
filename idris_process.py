"""
Inspired by 
https://github.com/idris-hackers/idris-bot/

"""

import subprocess
import time

import idris_parse_result_command as parse

class IdrisProcess(subprocess.Popen):
	"""docstring for IdrisProcess"""

	template_stdin = '((:interpret "{cmd}") 0)\n'

	def __init__(self):
		super(IdrisProcess, self).__init__(
			[
				"idris",
				"--ide-mode",
				"--nocolor"
			],
			stdin  = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.DEVNULL
		)

	def send_cmd(self, cmd):
		command        = IdrisProcess.template_stdin.format(cmd = cmd)
		length_request = len(command) 

		to_send = bytes("{:06x}".format(length_request) + command, "utf-8")

		self.stdin.write(to_send)
		self.stdin.flush()

	def receive_cmd(self):
		length = int(self.stdout.read(6).decode("utf8"), base = 16)
		result = self.stdout.read(length)
		return parse.parse_expr(result.decode("utf8"))

	def first_interpretable_cmd(self):

		pass

def interpret_cmd(expr):
	if expr.type != parse.Type.Expr:
		return None

	if len(symbol.obj) <= 1:
		return None
		
	symbol = expr.obj[0]
	args    = expr.obj[1]
	if symbol.type != parse.Type.Symbol:
		return None

	if symbol.obj == "return":
		if args.type != parse.Type.Expr:
			return None
		if len(args.obj) <= 1:
			return None
		if args.obj[0].type != parse.Type.Symbol:
			return None
		if args.obj[1].type != parse.Type.String:
			return None

		status = args.obj[0].obj
		output = args.obj[1].obj

	elif symbol.obj == "write-string":
		if args.type != parse.Type.String:
			return None
		output = args.obj
		

	return None

process = IdrisProcess()





