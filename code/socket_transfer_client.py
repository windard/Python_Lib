# -*- coding: utf-8 -*-

import os
import struct
import socket
import hashlib


host = "127.0.0.1"
port = 8081


class TransferFile(object):
    def __init__(self, filename, path=None):
        self.content = ''
        self.filename = self.fullname = os.path.abspath(filename)
        if path:
            self.fullname = os.path.join(path, filename)
        self.filename = os.path.basename(self.fullname)

    @property
    def exists(self):
        return os.path.exists(self.fullname)

    @property
    def md5(self):
        return hashlib.md5(self.content).hexdigest()

    @property
    def size(self):
        return len(self.content)

    def save(self):
        with open(self.fullname, 'wb') as f:
            f.write(self.content)

    def open(self):
        with open(self.fullname, 'rb') as f:
            self.content = f.read()

    def delete(self):
        return os.remove(self.fullname)


def transfer_file(conn):
    file_path = raw_input("File path:")
    tf = TransferFile(file_path)
    if not tf.exists:
        print('file not exists')
        return
    tf.open()
    conn.sendall(struct.pack('128sl32s', tf.filename, tf.size, tf.md5))
    flag = conn.recv(1024)
    if flag == 'ok':
        with open(tf.fullname, 'rb') as f:
            while 1:
                piece = f.read(1024)
                if not piece:
                    break
                conn.sendall(piece)
        print 'file transfer success.'
    else:
        print flag
    last = conn.recv(1024)
    print last


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    buf = s.recv(1024)
    print(buf)
    transfer_file(s)


if __name__ == '__main__':
    main()
