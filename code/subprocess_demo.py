# coding=utf-8
import os
import six
import subprocess

if six.PY2:
    input = raw_input
cwd = os.getcwd()


def run_command(command):
    global cwd
    command = command.rstrip()
    commands = command.split()
    if commands and commands[0] == "cd":
        cwd = (len(commands) > 1 and os.path.join(cwd, commands[1])) or os.path.expanduser('~')
        return b""

    try:
        process = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True, cwd=cwd)
        stdout, stderr = process.communicate()
        retcode = process.poll()
        if retcode:
            return stderr
        return stdout
    except:
        output = 'Failed to execute command.\r\n'

    return output


if __name__ == '__main__':
    while 1:
        command = input("$ ")
        if command == "exit" or command == "quit":
            break
        result = run_command(command)
        
        print(result.decode("utf-8"))
