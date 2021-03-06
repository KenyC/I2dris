from ipykernel.kernelbase import Kernel
import pygments.lexers.haskell as lexers

import idr_parse.interpret as interpret
import idr_parse           as expr
import process
import parse               


class IdrisKernel(Kernel):
	implementation           = "i2dris"
	implementation_version   = "0.0"
	language                 = "Idris"
	language_version         = "1.3"
	banner                   = "i2dris - A kernel for Idris"

	language_info = {
		"mimetype"       : "text/x-idris",
		"file_extension" : "idr",
		"name"           : "idris"
	}

	def __init__(self, *args, **kwargs):
		self.idris_process = process.IdrisProcess()
		# self.tmp_directory = tempfile.TemporaryDirectory()
		super(IdrisKernel, self).__init__(*args, **kwargs)


	int_to_cmd = [":let\n", "", "", ":unlet "]
	def do_execute(self,
		           code, 
		           silent, 
		           store_history    = True,
		           user_expressions = None,
		           allow_stdin      = False):


		status = "ok" 
		cmds = parse.parse_code_into_codetypes(code)
		# self.output(cmds)

		for cmd_type, content in cmds:

			self.idris_process.interpret_(IdrisKernel.int_to_cmd[cmd_type] + content)
			output_results = silent or cmd_type == parse.CodeType.Undeclare


			while True:
				output = self.idris_process.receive_cmd()
				interpreted_result = interpret.interpret(output)

				if interpreted_result is not None:

					if isinstance(interpreted_result, interpret.WriteString):
						self.output(interpreted_result.to_write, output_results)

					elif isinstance(interpreted_result, interpret.Warning):
						self.output(interpreted_result.error, output_results)

					elif isinstance(interpreted_result, interpret.Return):
						status = interpreted_result.status
						if interpreted_result.message is not None:
							self.output(interpreted_result.message, output_results)

						break
					else:
						status = "error"
						break
			# Ignore errors due to undeclare inexisting variables
			if status == "error" and cmd_type != parse.CodeType.Undeclare:
				break


		# file_path = os.path.join(self.tmp_directory.name, "tmp.idr")
		# file_path = "tmp.idr"
		# with 
		# with tempfile.NamedTemporaryFile("w", suffix = ".idr", dir = self.tmp_directory.name) as f:
		# 	f.write(code)
		# 	f.flush()

		# 	# result = self.idris_process.load_file_(file_path)
		# 	result = self.idris_process.load_file_(f.name)

		# 	while True:
		# 		output = self.idris_process.receive_cmd()
		# 		result = process.IdrisProcess.interpret_result(output)

		# 		self.output(str(output) + "\n", silent)
		# 		if result is not None:
		# 			status, message = result

		# 			if status != "put":
		# 				break


		return {
			"status":           status,
			"execution_count":  self.execution_count,
			"payload":          [],
			"user_expressions": {},
		}

	def output(self, message, silent = False):
		if not silent:
			stream_content = {'name': 'stdout', 'text': str(message)}
			self.send_response(self.iopub_socket, 'stream', stream_content)

	def do_shutdown(self, restart):
		self.idris_process.terminate()
		try:
			self.idris_process.wait(3)
		except:
			self.idris_process.kill()

		return {
			'status'  : 'ok', 
			'restart' : restart
		}


if __name__ == '__main__':
	from ipykernel.kernelapp import IPKernelApp
	IPKernelApp.launch_instance(kernel_class = IdrisKernel)
