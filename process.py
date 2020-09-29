"""
Inspired by 
https://github.com/idris-hackers/idris-bot/

Info about IDE mode and what commands can be sent to it is available at:
https://github.com/idris-lang/Idris-dev/blob/master/src/Idris/IdeMode.hs

"""

import subprocess
import time

import idr_parse as parse
import idr_parse.interpret as interpret

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
		self.first_interpretable_cmd()

	def receive_cmd(self, timeout = 10):
		length = int(self.stdout.read(6).decode("utf8"), base = 16)
		result = self.stdout.read(length)

		result, couldnt_parse = parse.parse_expr(result.decode("utf8").strip())
		if couldnt_parse:
			print("Couldn't parse", couldnt_parse)
		return result

	def first_interpretable_cmd(self, output = print):
		while True:
			unparsed_result = self.receive_cmd()
			interpreted_result = interpret.interpret(unparsed_result)

			if interpreted_result is not None:

				output(interpreted_result)

				if isinstance(interpreted_result, interpret.Return):
					break



if __name__ == "__main__":
	process = IdrisProcess()

	code1 = """Int'' : Type
Int'' = (a : Type) -> (a -> a) -> a -> a

successor : Int'' -> Int''
"""

	code2 = """recursion_over_int : Int'' -> (a : Type) -> ((a, Int'') -> a) -> a -> a
recursion_over_int n a inheritance initial = fst $ n (a, Int'') inheritance2 (initial, zero)
                                             where 
                                             inheritance2 : (a, Int'') -> (a, Int'')
                                             inheritance2 (x, m) = (inheritance (x, m), succ m)
"""
	print(code1)
	print(code2)




