# -*- coding: utf-8 -*-

import urllib2

# first try
try:
    resp = urllib2.urlopen("http://httpbin.org/basic-auth/admin/password")
    print resp.read()
except Exception as e:
    print "error", e


# with basic auth
basic_auth = urllib2.HTTPBasicAuthHandler()
basic_auth.add_password(
    realm="Fake Realm",  # 资源域空间
    uri="http://httpbin.org/basic-auth/admin/password",  # 资源地址
    user='admin',  # 用户名
    passwd='password'  # 密码
)

opener = urllib2.build_opener(basic_auth)
urllib2.install_opener(opener)


# second try
try:
    resp = urllib2.urlopen("http://httpbin.org/basic-auth/admin/password")
    print resp.read()
except Exception as e:
    print "error", e
