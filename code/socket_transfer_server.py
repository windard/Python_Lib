# -*- coding: utf-8 -*-

import os
import socket
import thread
import struct
import hashlib

host = "127.0.0.1"
port = 8081


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    print "Server is running on %s:%s Press Ctrl-C to stop" % (host, port)

    while 1:
        clientsock, clientaddr = s.accept()
        thread.start_new_thread(connect, (clientsock, clientaddr))


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


def connect(clientsock, clientaddr):
    print "Welcome from %s : %s" % (clientaddr[0], clientaddr[1])
    clientsock.sendall("File Transfer Server")
    filemeta = clientsock.recv(1024)
    filename, filesize, filemd5 = struct.unpack('128sl32s', filemeta)
    filename = filename.strip('\x00')
    print('receive file %s' % filename)
    tf = TransferFile(filename)
    if tf.exists:
        print 'file already exists'
        clientsock.sendall('exists')
        clientsock.close()
        return
    else:
        tf.content = ''
        clientsock.sendall('ok')
    while filesize > tf.size:
        piece = clientsock.recv(1024)
        tf.content += piece
    if tf.size == filesize and tf.md5 == filemd5:
        print 'file transfer success'
        tf.save()
    else:
        print 'file transfer fail'
    clientsock.sendall('roger')
    clientsock.close()


if __name__ == '__main__':
    main()
