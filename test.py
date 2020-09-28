import tempfile

import idris_process as process

idris_process = process.IdrisProcess()
code = """
a : Bool\n
a = True
"""

directory = tempfile.TemporaryDirectory()

with tempfile.NamedTemporaryFile("w", suffix = ".idr", dir = directory.name) as f:
	f.write(code)
	f.flush()
	result = idris_process.load_file(f.name)

print(result)

