"""
Inspired by 
https://github.com/idris-hackers/idris-bot/

Info about IDE mode and what commands can be sent to it is available at:
https://github.com/idris-lang/Idris-dev/blob/master/src/Idris/IdeMode.hs

"""

import subprocess
import time

import idr_parse as parse

class IdrisProcess(subprocess.Popen):
	"""Start & communicate with Idris process"""

	template_interpret  = '((:interpret "{cmd}") 0)\n'
	template_loadfile   = '((:load-file "{file}") 0)\n'

	def __init__(self):
		super(IdrisProcess, self).__init__(
			[
				"idris",
				"--ide-mode",
				"--nocolor"
			],
			stdin         = subprocess.PIPE,
			stdout        = subprocess.PIPE,
			stderr        = subprocess.STDOUT
		)

	def load_file(self, file):
		return self.send_cmd(IdrisProcess.template_loadfile.format(file = file))

	def interpret(self, cmd):
		return self.send_cmd(IdrisProcess.template_interpret.format(cmd = cmd))

	def load_file_(self, file):
		return self.send_cmd_(IdrisProcess.template_loadfile.format(file = file))

	def interpret_(self, cmd):
		return self.send_cmd_(IdrisProcess.template_interpret.format(cmd = cmd))

	def send_cmd_(self, cmd):
		length_request = len(cmd) 

		to_send = bytes("{:06x}".format(length_request) + cmd, "utf-8")

		self.stdout.flush()
		self.stdin.write(to_send)
		self.stdin.flush()

	def send_cmd(self, cmd):
		self.send_cmd_(cmd)
		return self.first_interpretable_cmd()

	def receive_cmd(self, timeout = 10):
		length = int(self.stdout.read(6).decode("utf8"), base = 16)
		result = self.stdout.read(length)

		result, couldnt_parse = parse.parse_expr(result.decode("utf8").strip())
		if couldnt_parse:
			print("Couldn't parse", couldnt_parse)
		return result

	def first_interpretable_cmd(self):
		while True:
			result = IdrisProcess.interpret_result(self.receive_cmd())
			if result is not  None:
				return result



	def interpret_result(expr):
		if expr is None or expr.type != parse.Type.Expr:
			return None

		symbol  = expr.obj[0]
		args    = expr.obj[1]

		if len(symbol.obj) <= 1:
			return None
		if symbol.type != parse.Type.Symbol:
			return None

		if symbol.obj == "return":
			if args.type != parse.Type.Expr:
				return None
			if len(args.obj) <= 1:
				return None
			if args.obj[0].type != parse.Type.Symbol:
				return None

			if args.obj[1].type == parse.Type.String:
				status = args.obj[0].obj
				output = args.obj[1].obj
			elif args.obj[1].type == parse.Type.Expr:
				status = args.obj[0].obj
				output = expr.__str__()
			else:
				return None

		elif symbol.obj == "write-string":
			if args.type != parse.Type.String:
				return None
			
			status = "put"
			output = args.obj
		elif symbol.obj == "warning":
			if args.type != parse.Type.String:
				return None
			
			status = "put"
			output = str(expr)
		else:
			return None
		

		return status, output

if __name__ == "__main__":
	process = IdrisProcess()





