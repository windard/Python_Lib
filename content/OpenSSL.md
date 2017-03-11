## OpenSSL

SSL ( Secure Sockets Layer) 也称为 TLS ( Transport Layer Security) ，是利用现代加密技术和密码认证技术来保障网络通信安全的技术，在网络上有广泛的应用。如 HTTPS，SSH，SMTP，openVPN，Git 等。

SSL 是采用的是 公钥加密技术，公钥加密技术中有一个密钥对，一个公钥和一个私钥。在加密时，采用公钥加密，私钥解密，在认证时则相反，采用私钥加密，公钥解密。

在一般使用 SSL 的时候，通常会有一个 证书授权机构 ( Certificate Authorities , CA )来负责颁发和验证证书，即服务器端的公钥。

首先我们来试一下使用 socket 内置的 SSL 模块。

```
# coding=utf-8

import socket,sys

def sendall(s,buf):
    bytewritten = 0
    while bytewritten < len(buf):
        bytewritten += s.write(buf[bytewritten:])

print "Create Socket ... "

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print "DONE"

print "Connecting to remote host ... "
s.connect(('www.baidu.com',443))
print "DONE"

print "Establishing SSL ... "
ssl = socket.ssl(s)
print   "DONE"

print "Requesting doument ... "
sendall(ssl,'GET / HTTP/1.0\r\n\r\n')
print   "DONE"

s.shutdown(1)

while 1:
    try:
        buf = ssl.read(1024)
    except socket.sslerror,err:
        if err[0] in [socket.SSL_ERROR_ZERO_RETURN,socket.SSL_ERROR_EOF]:
            break
        elif err[0] in [socket.SSL_ERROR_WANT_READ,socket.SSL_ERROR_WANT_WRITE]:
            continue
        raise
    if len(buf) == 0:
        break
    sys.stdout.write(buf)

s.close()

```

