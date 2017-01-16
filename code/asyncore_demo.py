# coding=utf-8

import socket, traceback, os, sys, select

class stateclass(object):
    """docstring for stateclass"""

    stdmask = select.POLLERR | select.POLLHUP | select.POLLNVAL

    def __init__(self, mastersock):
        self.mastersock = mastersock
        self.p = select.poll()
        self.watchread(mastersock)
        self.buffers = {}
        self.sockets = {mastersock.fileno():mastersock}

    def fd2socket(self, fd):
        return self.sockets[fd]

    def watchread(self, fd):
        self.p.register(fd, select.POLLIN|self.stdmask)

    def watchwrite(self, fd):
        self.p.register(fd, select.POLLOUT|self.stdmask)

    def watchboth(self, fd):
        self.p.register(fd, select.POLLIN|select.POLLOUT|self.stdmask)

    def dontwatch(self, fd):
        self.p.unregister(fd)

    def newconn(self, sock):
        fd = sock.fileno()
        self.watchboth(fd)
        self.buffers[fd] = 'Welcome to the echoserver,%s\n'%str(sock.getpeername())
        self.sockets[fd] = sock

    def readevent(self, fd):
        try:
            self.buffers[fd] += self.fd2socket(fd).recv(4096)
        except:
            self.closeout(fd)
        self.watchboth(fd)

    def writeevent(self, fd):
        if not len(self.buffers[fd]):
            self.watchread(fd)
            return

