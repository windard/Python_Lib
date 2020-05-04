# -*- coding: utf-8 -*-

import cookielib
import urllib2


def creat_cookie(name, value, **kwargs):
    result = {
        'version': 0,
        'name': name,
        'value': value,
        'port': None,
        'domain': '',
        'path': '/',
        'secure': False,
        'expires': None,
        'discard': True,
        'comment': None,
        'comment_url': None,
        'rest': {'HttpOnly': None},
        'rfc2109': False,
    }
    result.update(kwargs)
    result['port_specified'] = bool(result['port'])
    result['domain_specified'] = bool(result['domain'])
    result['domain_initial_dot'] = result['domain'].startswith('.')
    result['path_specified'] = bool(result['path'])

    return cookielib.Cookie(**result)


def header():
    cookie_jar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_handler)

    request = urllib2.Request("http://httpbin.org/cookies")
    request.add_header("Cookie", "name=windard")

    resp = opener.open(request)
    print resp.read()

    for cookie in cookie_jar:
        print cookie.name, ":", cookie.value


def main():
    cookie_jar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    opener = urllib2.build_opener(cookie_handler)
    cookie_jar.set_cookie(creat_cookie("name", "Windard"))
    cookie_jar.set_cookie(creat_cookie("location", "Shanghai"))

    resp = opener.open("http://httpbin.org/cookies")
    print resp.read()

    for cookie in cookie_jar:
        print cookie.name, ":", cookie.value


if __name__ == '__main__':
    header()
