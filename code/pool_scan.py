# -*- coding: utf-8 -*-

import socket
import multiprocessing
from multiprocessing.pool import ThreadPool


ip2num = lambda x: sum(
    [256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
num2ip = lambda x: '.'.join(
    [str(x / (256 ** i) % 256) for i in range(3, -1, -1)])


def scan(data):
    host, port, show = data
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


def udp_scan(data):
    host, port, show = data
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


def collect_data(host=None, host_start=None, host_end=None, port_start=None,
           port_end=None, show=None):
    data = []
    if host:
        for port in xrange(port_start, port_end):
            data.append((num2ip(host), port, show))
    else:
        for host in xrange(ip2num(host_start), ip2num(host_end)):
            for port in xrange(port_start, port_end):
                data.append((num2ip(host), port, show))
    return data


def port_scan(host, host_start, host_end, port, port_start, port_end,
              thread_num, show, udp):
    if port != 0:
        if host != '127.0.0.1':
            data = collect_data(host, None, None, port, port + 1, show)
        else:
            data = collect_data(None, host_start, host_end, port, port + 1, show)
    else:
        if host != '127.0.0.1':
            data = collect_data(host, None, None, port_start, port_end, show)
        else:
            data = collect_data(None, host_start, host_end, port_start, port_end, show)

    # p = ThreadPool(thread_num)
    p = multiprocessing.Pool(thread_num)
    if udp:
        p.map_async(udp_scan, data)
    else:
        p.map_async(scan, data)
    p.close()
    p.join()


if __name__ == '__main__':
    port_scan('127.0.0.1', '127.0.0.1', '127.0.0.2', 0, 0, 15535, 5, False, False)
