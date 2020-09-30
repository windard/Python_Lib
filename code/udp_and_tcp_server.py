# -*- coding: utf-8 -*-

import socket
import select

host = '127.0.0.1'
port = 8780

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((host, port))
tcp_server.listen(5)

udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind((host, port))

inputs = [tcp_server, udp_server]

if __name__ == '__main__':

    print("Concurrent Listening on {}:{}, Press Ctrl-C to stop".format(host, port))

    while True:
        rs, ws, es = select.select(inputs, [], [])
        for r in rs:
            if r is tcp_server:
                c, addr = tcp_server.accept()
                print('[TCP] Got connection from {}:{}'.format(*addr))
                inputs.append(c)
            elif r is udp_server:
                data, addr = udp_server.recvfrom(1024)
                print('[UDP] Got message: {} from {}:{}'.format(data, *addr))
                udp_server.sendto('[UDP] {}'.format(data), addr)
            else:
                try:
                    data = r.recv(1024)
                    disconnected = not data
                except socket.error:
                    disconnected = True

                if disconnected:
                    print('[TCP] {}:{} disconnected.'.format(*r.getpeername()))
                    inputs.remove(r)
                else:
                    print('[TCP] Got message: {} from {}:{}'.format(data, *r.getpeername()))
                    r.send('[TCP] {}'.format(data))
