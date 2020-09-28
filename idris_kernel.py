from ipykernel.kernelbase import Kernel
import os.path
import tempfile

import idris_process as process

class IdrisKernel(Kernel):
	implementation           = "i2dris"
	implementation_version   = "0.0"
	language                 = "Idris"
	language_version         = "1.3"
	banner                   = "i2dris - A kernel for Idris"

	language_info = {
		"mimetype"       : "text/plain",
		"file_extension" : "idr"
		#"pygments_lexer" : todo
	}

	def __init__(self, *args, **kwargs):
		self.idris_process = process.IdrisProcess()
		self.tmp_directory = tempfile.TemporaryDirectory()
		super(IdrisKernel, self).__init__(*args, **kwargs)


	def do_execute(self,
		           code, 
		           silent, 
		           store_history    = True,
		           user_expressions = None,
		           allow_stdin      = False):

		# file_path = os.path.join(self.tmp_directory.name, "tmp.idr")
		# file_path = "tmp.idr"
		# with 
		with tempfile.NamedTemporaryFile("w", suffix = ".idr", dir = self.tmp_directory.name) as f:
			f.write(code)
			f.flush()

			# result = self.idris_process.load_file_(file_path)
			result = self.idris_process.load_file_(f.name)

			while True:
				output = self.idris_process.receive_cmd()
				result = process.IdrisProcess.interpret_result(output)

				self.output(str(output) + "\n", silent)
				if result is not None:
					status, message = result

					if status != "put":
						break



		return {
			"status":           "ok",
			"execution_count":  self.execution_count,
			"payload":          [],
			"user_expressions": {},
		}

	def output(self, message, silent = False):
		if not silent:
			stream_content = {'name': 'stdout', 'text': str(message)}
			self.send_response(self.iopub_socket, 'stream', stream_content)

	def do_shutdown(self, *args, **kwargs):
		print("I ended rather gracefully.")
		self.idris_process.terminate()


if __name__ == '__main__':
	from ipykernel.kernelapp import IPKernelApp
	IPKernelApp.launch_instance(kernel_class = IdrisKernel)
