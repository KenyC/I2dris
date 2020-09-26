from IPython.kernel.zmq.kernelbase import Kernel
import subprocess

class IdrisKernel(Kernel):
	implementation           = "i2dris"
	implementation_version   = "0.0"
	language                 = "Idris"
	language_version         = "1.3"
	banner                   = "i2dris 0.0"

	language_info = {
		"mimetype"       : "text/plain"
		"file_extension" : "idr"
		#"pygments_lexer" : todo
	}

	def __init__(self, *args, **kwargs):
		super(IdrisKernel, self).__init__(*args, **kwargs)
		self.idris_server = subprocess.Popen([
			"idris"
		], stdin = subprocess.DEVNULL)


	def do_execute(self,
		           code, 
		           silent, 
		           store_history    = True,
		           user_expressions = None,
		           allow_stdin      = False):


		return {
			"status":           "ok",
			"execution_count":  self.execution_count,
			"payload":          [],
			"user_expressions": {},
		}

	def do_shutdown(self):
		print("I ended rather gracefully.")
		self.idris_server.kill()


if __name__ == '__main__':
	from IPython.kernel.zmq.kernelapp import IPKernelApp
	IPKernelApp.launch_instance(kernel_class = EchoKernel)
