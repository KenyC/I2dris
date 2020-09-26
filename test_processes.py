import subprocess
import time

fout = open("output.txt", "wb")
ferr = open("error.txt", "wb")

process = subprocess.Popen([
		"idris",
		"--nocolor",
		"--ide-mode"
	],
	stdin  = subprocess.PIPE,
	stdout = fout,
	stderr = ferr
)

template_stdin = '((:interpret "{cmd}") 0)\n'
def send_request_to_process(receiver, request):
	command        = template_stdin.format(cmd = request)
	length_request = len(command) 

	to_send = bytes("{:06x}".format(length_request) + command, "utf-8")
	print(to_send)
	# return to_send
	receiver.stdin.write(to_send)
	receiver.stdin.flush()



send_request_to_process(process, ":consolewidth 45")
send_request_to_process(process, ":t a")


# process.stdin.close()
time.sleep(2)
process.terminate()
process.wait(3)

fout.close()
ferr.close()
"""
sendQuery ":consolewidth 18" 0

longueurhexadecimal ((interpret :consolewidth 18) 0)
"""