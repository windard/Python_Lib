# -*- coding: utf-8 -*-

import sys
import socket
import select
import argparse


def runserver(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(10)

    print "Server is running ... "

    inputs = [sys.stdin, s]
    outputs = []
    clients = {}

    while True:
        try:
            readable, writeable, exceptional = select.select(inputs, outputs, [])
            for sock in readable:
                # client 连接
                if sock == s:
                    clientsock, clientaddr = sock.accept()
                    recvname = clientsock.recv(1024)
                    if recvname.endswith("NAME:"):
                        clientname = str(clientaddr)
                    else:
                        clientname = recvname.split('NAME:')[1]
                    clientsock.sendall("Welcome " + clientname + "\n")
                    print clientname + " Come In"
                    clients[clientsock] = (clientname, clientaddr, clientsock)
                    inputs.append(clientsock)
                    for output in outputs:
                        output.sendall("Welcome " + clientname + " Come In \n")
                    outputs.append(clientsock)
                # server 说话
                elif sock == 0 or isinstance(sock, file):
                    message = sys.stdin.readline()
                    if message.startswith("QUIT"):
                        print "Server is close ... "
                        sys.exit(0)
                    for output in outputs:
                        output.sendall("Server : " + message)
                # server 接收数据
                else:
                    data = sock.recv(1024)
                    # 接收到数据就是有人说话
                    if data:
                        if data.startswith("SECRECT"):
                            print "SECRECT " + clients[sock][0] + " : " + data,
                            output = data.split(" ")[1]
                            message = data.split(" ")[2]
                            for client in clients.values():
                                if client[0] == output:
                                    client[2].sendall("SECRECT " + clients[sock][0] + " : " + message)
                        else:
                            print clients[sock][0] + " : " + data,
                            for output in outputs:
                                if output != sock:
                                    output.sendall(clients[sock][0] + " : " + data)
                    # 没接收到数据就是有人离开
                    else:
                        name = clients[sock][0]
                        print name + " leaved "
                        for output in outputs:
                            output.sendall(name + " leaved \n")
                        inputs.remove(sock)
                        outputs.remove(sock)
                        del clients[sock]

        except KeyboardInterrupt:
            print "Server is close ... "
            break


def runclient(host, port, name=None):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((host, port))
    if name is not None:
        s.sendall("NAME:" + name)
    else:
        s.sendall("NAME:")

    print s.recv(1024),

    while True:
        try:
            readable, writeable, exceptional = select.select([0, s], [], [])
            for sock in readable:
                if sock == s:
                    data = sock.recv(1024)
                    if not data:
                        print "Server is closed"
                        sys.exit(0)
                    sys.stdout.write(data)
                    sys.stdout.flush()
                else:
                    data = sys.stdin.readline()
                    if data.startswith("QUIT"):
                        print "Client is closed"
                        sys.exit(0)
                    s.sendall(data)
        except KeyboardInterrupt:
            print "Client is closed"
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="socket chatroom")
    parser.add_argument("--type", help="chose the type", action="store", default="client", dest="type")
    parser.add_argument("--host", help="input your host", action="store", default="127.0.0.1", dest="host")
    parser.add_argument("--port", help="input your port", action="store", default=8888, type=int, dest="port")
    parser.add_argument("--name", help="input your name", action="store", default=None, dest="name")
    args = parser.parse_args()
    chattype = args.type
    host = args.host
    port = args.port
    name = args.name
    if chattype.startswith("server"):
        runserver(host, port)
    elif chattype.startswith("client"):
        runclient(host, port, name)
    else:
        print "your input is wrong"
