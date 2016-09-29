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
http://resource.xidian.edu.cn/announce.php?passkey=9c0de35d732fe76d3b4fd2e8157db8b9
True
windard@windard:~/Desktop/python$ python libtorrent_demo.py
The.Garden.of.Words.2013.BluRay.1080p.10bit.x264.FLAC.DTS.AC3.6Audio-NYHD.mkv
8ae7e343ae7a0ea5ceb600afc38efc0e6876c144
4445065381
1
4445065381 The.Garden.of.Words.2013.BluRay.1080p.10bit.x264.FLAC.DTS.AC3.6Audio-NYHD.mkv
爱生活 爱西电 爱睿思
uTorrent/3200
http://resource.xidian.edu.cn/announce.php?passkey=9c0de35d732fe76d3b4fd2e8157db8b9
True
```

#### 种子与磁力链接转换

使用 libtorrent 就可以非常简单的进行转换，或者是使用 bencode

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

###### 磁力链接转种子

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
