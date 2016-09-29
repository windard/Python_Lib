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

