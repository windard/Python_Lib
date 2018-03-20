## ipaddress

IPAddress 解析库

```
def ip2hex(ip, encoding='utf-8'):
    if type(ip) in [bytes, str]:
        ip = ip.decode(encoding)
    elif type(ip) not in [unicode]:
        raise ValueError("IPAddress not valid")
    ip_address = ipaddress.ip_address(ip)
    return ip_address.packed.encode('hex')


def hex2ip(ip):
    return str(ipaddress.ip_address(int(ip, 16)))


def hex2ip_old(ip):
    return ".".join(map(str, map(lambda x: int(x, 16),
                                 [ip[i:i+2] for i in xrange(0, len(ip), 2)])))


def ip2hex_old(ip):
    return "%02x%02x%02x%02x" % tuple(map(int, ip.split('.')))


def int2ip(ip):
    return str(ipaddress.ip_address(ip))


def ip2int(ip, encoding='utf-8'):
    if type(ip) in [bytes, str]:
        ip = ip.decode(encoding)
    elif type(ip) not in [unicode]:
        raise ValueError("IPAddress not valid")
    return int(ipaddress.ip_address(ip))


def parse_peers(peers):
    ip, port = peers[:8], peers[8:]
    return '{}:{}'.format(hex2ip(ip), int(port, 16))


def combine_peers(peers):
    ip, port = peers.split(":")
    return '%s%04x' % (ip2hex(ip), int(port))

```
