# coding=utf-8

from gevent import monkey


monkey.patch_all()

from gevent.pool import Pool
import socket


def scan(args):
    host, port, show = args
    s = socket.socket()
    protocolname = 'tcp'
    s.settimeout(0.1)
    if s.connect_ex((host, port)) == 0:
        try:
            print "%s:%4d open => service name: %s" % (
                host, port, socket.getservbyport(port, protocolname))
        except:
            print '%s:%4d open => service name: No Found' % (host, port)
    elif show:
        print port, 'Close'
    s.close()


def scan_all(start, end, host):
    pool = Pool(500)
    pool.map(scan, [(host, port, False) for port in xrange(start, end)])
    pool.join()


if __name__ == '__main__':
    scan_all(0, 10000, '127.0.0.1')
