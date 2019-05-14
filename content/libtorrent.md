## libtorrent

这是一个种子解析的 python 库，就可以用这个库来实现 P2P 文件传输。

LibTorrent 是一个C++ 语言的 BitTorrent 开发库，支持 Linux/Unix 系统。

LibTorrent 是一个C++ 语言的 BitTorrent 开发库，支持 Linux/Unix 系统。旨在提供高性能和良好代码风格的 BT 开发包。该开发包与其他包不同的是，它直接通过网络堆栈抓取文件页，因此性能是官方客户端的三倍。

所以这个第三方库也并没有在 pypi 源里，在 ubuntu 下可以通过 `sudo apt-get install python-libtorrent` 来安装。

#### 查看种子文件的信息

```
# coding=utf-8

import libtorrent as lt

info = lt.torrent_info('test.torrent')

# 文件名
name = info.name()
print name

# 文件 Hash
file_hash = info.info_hash()
print file_hash

# 总大小
total_size = info.total_size()
print total_size

# 文件总数
file_num = info.num_files()
print file_num

# 每个文件
for item in info.files():
    print item.size,item.path

# 注释
comment = info.comment()
print comment

# 创建时间 但是在我的电脑上报错
# date = info.creation_date()

# 创建者
creator = info.creator()
print creator

# 文件位置 但是还是在我的电脑上报错
# file_at = info.file_at()

# trackers
for x in info.trackers():
    print x.url

# 是否为私密种子
print info.priv()

# 返回DHT初始node
info.nodes()

# 分片SHA1值
info.pieces()

```

结果为

```
windard@windard:~/Desktop/python$ python libtorrent_demo.py
The.Garden.of.Words.2013.BluRay.1080p.10bit.x264.FLAC.DTS.AC3.6Audio-NYHD.mkv
8ae7e343ae7a0ea5ceb600afc38efc0e6876c144
4445065381
1
4445065381 The.Garden.of.Words.2013.BluRay.1080p.10bit.x264.FLAC.DTS.AC3.6Audio-NYHD.mkv 爱生活 爱西电 爱睿思
uTorrent/3200
http://resource.xidian.edu.cn/announce.php?passkey=xxxx
True
```

#### 手动编解码种子文件

bt 种子文件是由 bencoding 编码的字典结构

##### bencoding 编码

Bencoding 主要用在种子文件中，也用于同 tracker 请求时的返回响应

bencoding 编码主要有四种数据结构 字符串，整数，列表和字典

- 整数: 整数以十进制编码并处在字符`i`和`e`之间，如 `0 -> i0e`, `42 -> i42e`, `-43 -> i-43e`
- 字符串: 字符串按 ASCII 编码之后以 `(长度):(内容)` 的格式编码，如 `'spam' -> 4:spam`
- 列表: 列表的内容处在字符`l`和`e`之间，元素格式为 bencoding 的四种编码格式，如 `[42, 'spam'] -> li42e4:spame`
- 字典: 字典的内容处在字符`d`和`e`之间，字典的键和值必须紧密相连且按照键值排序编码，如`{'bar':'spam', 'foo':42} -> d3:bar4:spam3:fooi42ee`

自己实现 bencoding 编码也不难，也有几个已有的库 `bencode`, `bencoder`, `libtorrent.bencode[bdecode]`, `bcoding`, `better_bencode`可以使用。

encode

```
# -*- coding: utf-8 -*-


class Encoder(object):
    code_method = None

    def __init__(self, raw_data, encoding='utf-8'):
        self.method = type(raw_data)
        self.raw_data = raw_data
        self.encoding = encoding

    def encode(self):
        raise NotImplementedError()


class IntegerEncoder(Encoder):
    code_method = [int, long]

    def encode(self):
        return 'i{}e'.format(self.raw_data)


class StringEncoder(Encoder):
    code_method = [str, unicode, bytes]

    def encode(self):
        if self.method == unicode:
            self.raw_data.encode(self.encoding)
        return '{}:{}'.format(len(self.raw_data), self.raw_data)


class ListEncoder(Encoder):
    code_method = [list, tuple, set]

    def encode(self):
        return 'l{}e'.format(''.join([encode(data) for data in self.raw_data]))


class DictEncoder(Encoder):
    code_method = [dict]

    def encode(self):
        self.raw_data = sorted(self.raw_data.items(), key=lambda a: a[0])
        return 'd{}e'.format(''.join([''.join(encode(item) for item in data)
                                      for data in self.raw_data]))


def encode(raw_data):
    method = type(raw_data)
    if method in IntegerEncoder.code_method:
        return IntegerEncoder(raw_data).encode()
    elif method in StringEncoder.code_method:
        return StringEncoder(raw_data).encode()
    elif method in ListEncoder.code_method:
        return ListEncoder(raw_data).encode()
    else:
        return DictEncoder(raw_data).encode()


if __name__ == '__main__':
    print encode(42)
    print encode('spam')
    print encode([42, 'spam'])
    print encode({'bar': 'spam', 'foo': 42})
    print encode({
        'encoding':'utf-8',
        'announce': ['http://baidu.com', 'http://ele.me'],
        'info': {
            'length': 123,
            'pieces': ['abc', 'def'],
            'name': 'secret star'
        }
    })

```


decode

```
# -*- coding: utf-8 -*-

import re


class Decoder(object):
    regex_text = None

    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.data = None

    def decode(self):
        raise NotImplementedError()


class IntegerDecoder(Decoder):

    regex_text = r'i([-]?[\d]+)e'

    def decode(self):
        value = re.match(self.regex_text, self.raw_data).group(1)
        self.raw_data = self.raw_data[1:]
        self.raw_data = self.raw_data.lstrip(value)
        self.raw_data = self.raw_data[1:]
        self.data = int(value)
        return self.raw_data, self.data


class StringDecoder(Decoder):

    regex_text = r'([\d]+):([\S]+)'

    def decode(self):
        length = re.match(self.regex_text, self.raw_data).group(1)
        self.raw_data = self.raw_data.lstrip(length)
        self.raw_data = self.raw_data.lstrip(':')
        self.data = self.raw_data[:int(length)]
        self.raw_data = self.raw_data[int(length):]
        return self.raw_data, self.data


class ListDecoder(Decoder):

    regex_text = r'l([\S]+)e'

    def __init__(self, raw_data):
        super(ListDecoder, self).__init__(raw_data)
        self.data = []

    def decode_item(self, raw_data):
        raw_data, value = decode(raw_data)
        self.data.append(value)
        return raw_data

    def decode(self):
        self.raw_data = self.raw_data[1:]
        while not self.raw_data.startswith('e'):
            self.raw_data = self.decode_item(self.raw_data)
        self.raw_data = self.raw_data[1:]
        return self.raw_data, self.data


class DictDecoder(Decoder):

    regex_text = r'd([\S]+)e'

    def __init__(self, raw_data):
        super(DictDecoder, self).__init__(raw_data)
        self.data = {}

    def decode_item(self, raw_data):
        raw_data, key = StringDecoder(raw_data).decode()
        raw_data, value = decode(raw_data)
        self.data[key] = value
        return raw_data

    def decode(self):
        self.raw_data = self.raw_data[1:]
        while not self.raw_data.startswith('e'):
            self.raw_data = self.decode_item(self.raw_data)
        self.raw_data = self.raw_data[1:]
        return self.raw_data, self.data


def decode(raw_data):
    if raw_data.startswith('d'):
        raw_data, data = DictDecoder(raw_data).decode()
    elif raw_data.startswith('l'):
        raw_data, data = ListDecoder(raw_data).decode()
    elif raw_data.startswith('i'):
        raw_data, data = IntegerDecoder(raw_data).decode()
    else:
        raw_data, data = StringDecoder(raw_data).decode()
    return raw_data, data


if __name__ == '__main__':
    # print decode('de')
    # print decode('i42e')
    # print decode('i42ee')
    # print decode('4:spam')
    # print decode('li42e4:spame')
    # print decode('d3:bar4:spam3:fooi42ee')
    print decode('d8:announcel16:http://baidu.com13:http://ele.mee8:encoding5:utf-84:infod6:lengthi123e4:name11:secret star6:piecesl3:abc3:defeee')  # noqa

```

##### 种子的字典结构

种子文件格式

- announce: tracker服务器的URL(字符串)
- announce-list(可选): 备用tracker服务器列表(列表)
- creation date(可选): 种子创建的时间，Unix 时间戳
- comment(可选): 备注(字符串)
- encoding: 编码方式(字符串)
- created by(可选): 创建人或创建程序的信息(字符串)
- info: 一个字典结构，包含文件的主要信息，为分二种情况：单文件结构或多文件结构

1.单文件结构如下：
 - length: 文件长度，单位字节(整数)
 - md5sum(可选): 长32个字符的文件的MD5校验和，BT不使用这个值，只是为了兼容一些程序所保留!(字符串)
 - name:文件名(字符串)
 - piece length: 每个块的大小，单位字节(整数)
 - pieces: 每个块的20个字节的SHA1 Hash的值(二进制格式)

2.多文件结构如下：
 - name:最上层的目录名字(字符串)
 - piece length: 每个块的大小，单位字节(整数)
 - files: 一个列表结构结构
  - length: 文件长度，单位字节(整数)
  - md5sum(可选): 同单文件结构中相同
  - path: 文件的路径和名字，是一个列表结构，如\test\test.txt 列表为l4:test8test.txte
 - pieces: 同单文件结构中相同

其结构大概就像这样

```
{
"announce"="http://btfans.3322.org:8000/announce"   ;tracker 服务器的URL(字符串)
"announce-list"=[["http://.."],["http://.."]]           ;备用tracker服务器列表(列表)，会覆盖 announce 字段
"creation date"=1175204110                          ;种子创建的时间，Unix标准时间格式
"encoding"="utf-8"                                  ;编码
"comment"="备注"
"created by"="创建人信息"

{

"info"={"files"=[{"filehash"="SHA1 Hash","length"=168099584,"path"=["01.rmvb"]},
                  {...},
                  {...}
                 ]

         "name"="保存目录名"
         "piece length"=2097152    ；每个块的大小，单位字节(整数)
         "pieces"="每个块的SHA1 Hash的值的顺序排列(二进制格式,长度为"20 X 块数")"


         }

}

}
```

实现种子文件的读取和写入和转磁力

```
# -*- coding: utf-8 -*-

import hashlib
from bencoding_encode import encode
from bencoding_decode import decode


def load(filename):
    data = open(filename, 'rb').read()
    return decode(data)[1]


def dump(filename, data):
    with open(filename, 'wb') as f:
        f.write(encode(data))


def torrent2magnet(filename):
    data = load(filename)
    return 'magnet:?xt=urn:btih:{}'.format(hashlib.sha1(encode(data['info'])).hexdigest())


if __name__ == '__main__':
    data = load('shape.torrent')
    dump('dump.torrent', data)
    print torrent2magnet('dump.torrent')

```


#### 种子与磁力链接转换

使用 libtorrent 就可以非常简单的进行转换，或者是使用 bencode

种子文件经过哈希算法可以直接组装成磁力链接，根据磁力链接需要向 tracker 请求或者经过 DHT 协议向其他用户获得种子内容

###### 种子文件转换为磁力链接

```
# coding=utf-8

import libtorrent as bt

info = bt.torrent_info('test.torrent')
print "magnet:?xt=urn:btih:%s&dn=%s" % (info.info_hash(), info.name())
```

或者是用 bencode

```
# coding=utf-8

import bencode, hashlib, urllib

torrent = open('test.torrent', 'rb').read()

metadata = bencode.bdecode(torrent)

hashcontents = bencode.bencode(metadata['info'])

digest = hashlib.sha1(hashcontents).hexdigest()

params = {'xt': 'urn:btih:%s' % digest,
                'dn': metadata['info']['name'],
                'tr': metadata['announce'],
                'xl': metadata['info']['length']}

paramstr = urllib.urlencode(params)

magneturi = 'magnet:?%s' % paramstr

print magneturi
```

###### 磁力链接转种子文件

```
# coding=utf-8

import shutil
import tempfile
import os.path as pt
import sys
import libtorrent as lt
from time import sleep

def magnet2torrent(magnet, output_name=None):
    if output_name and not pt.isdir(output_name) and not pt.isdir(pt.dirname(pt.abspath(output_name))):
        print("Invalid output folder: " + pt.dirname(pt.abspath(output_name)))
        sys.exit(0)
    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'duplicate_is_error': True,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, magnet, params)
    print("Downloading Metadata (this may take a while)")
    while (not handle.has_metadata()):
        try:
            sleep(1)
            print "Waiting ... "
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            print("Cleanup dir " + tempdir)
            shutil.rmtree(tempdir)
            sys.exit(0)
    ses.pause()
    print("Done")
    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)
    output = pt.abspath(torinfo.name() + ".torrent")
    if output_name:
        if pt.isdir(output_name):
            output = pt.abspath(pt.join(output_name, torinfo.name() + ".torrent"))
        elif pt.isdir(pt.dirname(pt.abspath(output_name))):
            output = pt.abspath(output_name)
            print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print("Saved! Cleaning up dir: " + tempdir)
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)
    return output

def showHelp():
    print("")
    print("USAGE: " + pt.basename(sys.argv[0]) + " MAGNET [OUTPUT]")
    print(" MAGNET\t- the magnet url")
    print(" OUTPUT\t- the output torrent file name")
    print("")

def main():
    # if len(sys.argv) < 2:
    #   showHelp()
    #   sys.exit(0)
    # magnet = sys.argv[1]
    # output_name = None
    # if len(sys.argv) >= 3:
    #   output_name = sys.argv[2]
    magnet = "magnet:?xt=urn:btih:C47C7F22ADEEDEFB6D5DACDD04F5CFAE298E0E23"
    output_name = "1.torrent"
    magnet2torrent(magnet, output_name)
    # magnet = "magnet:?dn=The.Garden.of.Words.2013.BluRay.1080p.10bit.x264.FLAC.DTS.AC3.6Audio-NYHD.mkv&tr=http%3A%2F%2Fresource.xidian.edu.cn%2Fannounce.php%3Fpasskey%3D9c0de35d732fe76d3b4fd2e8157db8b9&xl=4445065381&xt=urn%3Abtih%3A8ae7e343ae7a0ea5ceb600afc38efc0e6876c144"
    # output_name = "1.torrent"
    # magnet2torrent(magnet, output_name)

if __name__ == "__main__":
    main()

```

#### 制作种子和使用下载文件

```
# coding=utf-8

import libtorrent as lt
import sys
import os
import time
from optparse import OptionParser
import socket
import struct
import fcntl

def get_interface_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                            ifname[:15]))[20:24])
def ip2long(ip):
    return reduce(lambda a,b:(a<<8)+b,[int(i) for i in ip.split('.')])


def get_wan_ip_address():
    interfaces = set(['eth0', 'eth1', 'eth2', 'eth3', 'em1', 'em2', 'em3', 'em4'])
    ip = ''
    for i in interfaces:
        try:
            ip = get_interface_ip(i)
            if (ip2long(ip) < ip2long('10.0.0.0') or ip2long(ip) > ip2long('10.255.255.255')) \
                and (ip2long(ip) < ip2long('172.16.0.0') or ip2long(ip) > ip2long('172.33.255.255')) \
                and (ip2long(ip) < ip2long('192.168.0.0') or ip2long(ip) > ip2long('192.168.255.255')):
                return ip
        except:
            pass

    return ip

def make_torrent(path, save):
    fs = lt.file_storage()
    lt.add_files(fs, path)
    if fs.num_files() == 0:
        print 'no files added'
        sys.exit(1)

    input = os.path.abspath(path)
    basename = os.path.basename(path)
    t = lt.create_torrent(fs, 0, 4 * 1024 * 1024)

    t.add_tracker("http://10.0.1.5:8760/announce")
    t.set_creator('libtorrent %s' % lt.version)

    lt.set_piece_hashes(t, os.path.split(input)[0], lambda x: sys.stderr.write('.'))
    sys.stderr.write('\n')

    save = os.path.dirname(input)
    save = "%s/%s.torrent" % (save, basename)
    f=open(save, "wb")
    f.write(lt.bencode(t.generate()))
    f.close()
    print "the bt torrent file is store at %s" % save


def dl_status(handle):
    while not (handle.is_seed()):
        s = handle.status()

        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\ractive_time: %d, %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d, seeds: %d) %s' % \
                (s.active_time, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, s.num_seeds, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(1)
def seed_status(handle, seedtime=100):
    seedtime = int(seedtime)
    if seedtime < 100:
        seedtime = 100
    while seedtime > 0:
        seedtime -= 1
        s = handle.status()

        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
        print '\rseed_time: %d, %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d, seeds: %d) %s' % \
                (s.active_time, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, s.num_seeds, state_str[s.state]),
        sys.stdout.flush()

        time.sleep(1)

def remove_torrents(torrent, session):
    session.remove_torrent(torrent)

def read_alerts(session):
    alert = session.pop_alert()
    while alert:
        #print alert, alert.message()
        alert = session.pop_alert()

def download(torrent, path, upload_rate_limit=0, seedtime=100):
    try:
        session = lt.session()
        session.set_alert_queue_size_limit(1024 * 1024)

        sts = lt.session_settings()
        sts.ssl_listen = False
        sts.user_agent = "Thunder deploy system"
        sts.tracker_completion_timeout = 5
        sts.tracker_receive_timeout = 5
        sts.stop_tracker_timeout = 5
        sts.active_downloads = -1
        sts.active_seeds = -1
        sts.active_limit = -1
        sts.auto_scrape_min_interval = 5
        sts.udp_tracker_token_expiry = 120
        sts.min_announce_interval = 1
        sts.inactivity_timeout = 60
        sts.connection_speed = 10
        sts.allow_multiple_connections_per_ip = True
        sts.max_out_request_queue = 128
        sts.request_queue_size = 3

        sts.use_read_cache = False
        session.set_settings(sts)

        session.set_alert_mask(lt.alert.category_t.tracker_notification | lt.alert.category_t.status_notification)
        session.set_alert_mask(lt.alert.category_t.status_notification)

        ipaddr = get_wan_ip_address()
        #print ipaddr
        if ipaddr == "":
            session.listen_on(6881, 6881)
        else:
            session.listen_on(6881, 6881, ipaddr)

        limit = int(upload_rate_limit)
        if limit>=100:
            session.set_upload_rate_limit(limit*1024)
            session.set_local_upload_rate_limit(limit*1024)
        print session.upload_rate_limit()
        torrent_info = lt.torrent_info(torrent)
        add_params = {
            'save_path': path,
            'storage_mode': lt.storage_mode_t.storage_mode_sparse,
            'paused': False,
            'auto_managed': True,
            'ti': torrent_info,
        }

        handle = session.add_torrent(add_params)

        read_alerts(session)
        st = time.time()
        dl_status(handle)
        et = time.time() - st
        print '\nall file download in %.2f\nstart to seeding\n' % et
        sys.stdout.write('\n')
        handle.super_seeding()
        seed_status(handle, seedtime)

        remove_torrents(handle, session)
        assert len(session.get_torrents()) == 0

    finally:
        print 'download finished'

if __name__ == '__main__':
    usage = """usage: %prog [options] \n \
      %prog -d -f <torrent file=""> -s <file save="" path="">\n \
      or \n \
      %prog -m -p <file or="" dir=""> -s <torrent save="" path="">\n"
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--download", dest="download",
            help="start to download file", action="store_false", default=True)
    parser.add_option("-f", "--file", dest="file",
            help="torrent file")
    parser.add_option("-u", "--upload", dest="upload",
            help="set upload rate limit, default is not limit", default=0)
    parser.add_option("-t", "--time", dest="time",
            help="set seed time, default is 100s", default=100)
    parser.add_option("-p", "--path", dest="path",
            help="to make torrent with this path")
    parser.add_option("-m", "--make", dest="make",
            help="make torrent", action="store_false", default=True)
    parser.add_option("-s", "--save", dest="save",
            help="file save path, default is store to ./", default="./")
    (options, args) = parser.parse_args()
    #download(sys.argv[1])
    if len(sys.argv) != 6 and len(sys.argv) != 4 and len(sys.argv) != 8 and len(sys.argv) != 10:
        parser.print_help()
        sys.exit()
    if options.download == False and options.file !="":
        download(options.file, options.save, options.upload, options.time)
    elif options.make == False and options.path != "":
        make_torrent(options.path, options.save)

```
