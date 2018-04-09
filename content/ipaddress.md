## ipaddress

IP Address 解析库

```
# -*- coding: utf-8 -*-

import struct
import ipaddress


def ip2hex(ip, encoding='utf-8'):
    if type(ip) in [bytes, str]:
        ip = ip.decode(encoding)
    elif type(ip) not in [unicode]:
        raise ValueError("IPAddress not valid")
    ip_address = ipaddress.ip_address(ip)
    return ip_address.packed.encode('hex')


def hex2ip(ip):
    return str(ipaddress.ip_address(int(ip, 16)))


def int2ip(ip):
    return str(ipaddress.ip_address(ip))


def ip2int(ip, encoding='utf-8'):
    if type(ip) in [bytes, str]:
        ip = ip.decode(encoding)
    elif type(ip) not in [unicode]:
        raise ValueError("IPAddress not valid")
    return int(ipaddress.ip_address(ip))


def hex2ip_old(ip):
    return ".".join(map(str, map(lambda x: int(x, 16),
                                 [ip[i:i + 2] for i in
                                  xrange(0, len(ip), 2)])))


def ip2hex_old(ip):
    return "%02x%02x%02x%02x" % tuple(map(int, ip.split('.')))


def ip2hex_struct(ip):
    ip = map(int, ip.split('.'))
    return struct.pack('BBBB', *ip).encode('hex')


def hex2ip_struct(ip):
    return '.'.join(map(str, struct.unpack('BBBB', ip.decode('hex'))))


def ip2int_old(ip):
    ip = map(int, ip.split('.'))
    return (ip[0] << 24) + (ip[1] << 16) + (ip[2] << 8) + ip[3]


def int2ip_old(ip):
    ip = '{:032b}'.format(ip)
    return '.'.join(map(str,
                        [int(ip[:8], 2), int(ip[8:16], 2), int(ip[16:24], 2),
                         int(ip[24:], 2)]))


def ip2int_struct(ip):
    ip = map(int, ip.split('.'))
    return struct.unpack('>I', struct.pack('>BBBB', *ip))[0]


def int2ip_struct(ip):
    return '.'.join(
        map(str, struct.unpack('BBBB', '{:x}'.format(ip).decode('hex'))))


def ip_int2hex(ip):
    return struct.pack('>I', ip).encode('hex')


def ip_hex2int(ip):
    return struct.unpack('>I', ip.decode('hex'))[0]


def parse_peers(peers):
    ip, port = peers[:8], peers[8:]
    return '{}:{}'.format(hex2ip(ip), int(port, 16))


def parse_peers_struct(peers):
    ip_port = struct.unpack('>BBBBH', peers.decode('hex'))
    return '{}.{}.{}.{}:{}'.format(*ip_port)


def combine_peers(peers):
    ip, port = peers.split(":")
    return '%s%04x' % (ip2hex(ip), int(port))


def combine_peers_struct(peers):
    ip, port = peers.split(':')
    ip = map(int, ip.split('.'))
    port = int(port)
    ip_port = ip + [port]
    return struct.pack('>BBBBH', *ip_port).encode('hex')


if __name__ == '__main__':
    # print ip2hex('127.12.13.14')
    # print ip2hex_struct('127.12.13.14')
    # print hex2ip('7f0c0d0e')
    # print hex2ip_struct('7f0c0d0e')
    # print ip2int('127.12.13.14')
    # print struct.unpack('BBBB', '7f0c0d0e'.decode('hex'))
    # print repr(struct.pack('>I', 10240099))
    # print struct.pack('BBBB', 127, 12, 13, 14).encode('hex')
    # print combine_peers('127.12.13.14:1234')
    # print struct.unpack('>BBBBH', '7f0c0d0e04d2'.decode('hex'))
    # print parse_peers_struct('7f0c0d0e04d2')
    # print struct.pack('>BBBBH', 127, 12, 13, 14, 1234).encode('hex')
    # print combine_peers_struct('127.12.13.14:1234')

    print ip2int('127.12.13.14')
    print ip2int_old('127.12.13.14')
    print int2ip_old(2131496206)
    print int2ip_struct(2131496206)
    print ip2int_struct('127.12.13.14')
    # print struct.unpack('BBBB', '{:x}'.format(2131496206).decode('hex'))
    # print struct.unpack('>I', '{:x}'.format(2131496206).decode('hex'))
    # print repr(struct.pack('>I', 2131496206))
    # print repr(struct.unpack('>I', '7f0c0d0e'.decode('hex')))
    # print struct.unpack('>I', struct.pack('>BBBB', 127, 12, 13, 14))
    print struct.pack('>I', 2131496206).encode('hex')
    print struct.unpack('>I', '7f0c0d0e'.decode('hex'))[0]

```
