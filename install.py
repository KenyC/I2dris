import os
import json

kernel_json = {
	"argv" :  [
		"python", 
		os.path.join(os.getcwd(), "kernel.py"), 
		"-f", 
		"{connection_file}"
	],
	"display_name"     : "Idris",
	"language"         : "idris",
	"name"             : "i2dris",
	"code_mirror_mode" : "haskell"
}


try:
	from jupyter_client.kernelspec import install_kernel_spec
except ImportError:
	from IPython.kernel.kernelspec import install_kernel_spec

from IPython.utils.tempdir import TemporaryDirectory

with TemporaryDirectory() as temp_directory:
	os.chmod(temp_directory, 0o755)  # Starts off as 700, not user readable

	with open(os.path.join(temp_directory, 'kernel.json'), 'w') as f:
		json.dump(kernel_json, f, sort_keys=True)

	kernel_name = kernel_json['name']

	install_kernel_spec(
		temp_directory, 
		kernel_name, 
		user    = True,
		replace = True
	)