# -*- coding: utf-8 -*-


import socket
import threading
from Queue import Queue


ip2num = lambda x: sum(
    [256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
num2ip = lambda x: '.'.join(
    [str(x / (256 ** i) % 256) for i in range(3, -1, -1)])


def scan(host, port, show):
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


def udp_scan(host, port, show):
    udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    protocolname = 'udp'
    udpsock.settimeout(0.6)
    freq = 0
    for j in xrange(3):
        udpsock.sendto("", (host, port))
        try:
            data, addr = udpsock.recvfrom(1024)
        except socket.timeout:
            freq += 1
        except Exception, e:
            if e.errno == 10054:
                pass
            else:
                print tuple(e)
    if freq == 3:
        try:
            print "%s:%4d open => udp service name: %s" % (
                host, port, socket.getservbyport(port, protocolname))
        except:
            print "%s:%4d open => udp service name: %s" % (
                host, port, "No Found")
    elif show:
        print port, 'Close'
    udpsock.close()


def writeQ(queue, host=None, host_start=None, host_end=None, port_start=None,
           port_end=None):
    if host:
        for port in xrange(port_start, port_end):
            queue.put((num2ip(host), port))
    else:
        for host in xrange(ip2num(host_start), ip2num(host_end)):
            for port in xrange(port_start, port_end):
                queue.put((num2ip(host), port))


def readQ(queue, show, udp):
    while not queue.empty():
        try:
            host, port = queue.get()
            if udp:
                udp_scan(host, port, show)
            else:
                scan(host, port, show)
        finally:
            queue.task_done()


def port_scan(host, host_start, host_end, port, port_start, port_end,
              thread_num, show, udp):
    q = Queue(500)
    if port != 0:
        if host != '127.0.0.1':
            threading.Thread(target=writeQ, args=(
                q, host, None, None, port, port + 1)).start()
        else:
            threading.Thread(target=writeQ, args=(
                q, None, host_start, host_end, port, port + 1)).start()
    else:
        if host != '127.0.0.1':
            threading.Thread(target=writeQ, args=(
                q, host, None, None, port_start, port_end)).start()
        else:
            threading.Thread(target=writeQ, args=(
                q, None, host_start, host_end, port_start, port_end)).start()

    for thread in xrange(thread_num):
        threading.Thread(target=readQ, args=(q, show, udp)).start()
    q.join()


if __name__ == '__main__':
    port_scan('127.0.0.1', '127.0.0.1', '127.0.0.2', 0, 0, 15535, 5,
              False, False)
