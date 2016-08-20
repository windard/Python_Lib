# coding=utf-8

import subprocess

def run_command(command):
    command = command.rstrip()
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command.\r\n'

    return output


if __name__ == '__main__':
	while 1:
		command = raw_input("$ ")
		if command == "exit" or command == "quit":
			break
		result = run_command(command)
		
		print result,