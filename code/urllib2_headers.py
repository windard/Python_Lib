# -*- coding: utf-8 -*-

import urllib
import urllib2


headers = {
    "From": "China",
    "Year": "2020",
}

data = {
    "name": "windard",
    "country": "china",
}

request = urllib2.Request("http://httpbin.org/post", headers=headers)
request.add_data(urllib.urlencode(data))
request.add_header("To", "USA")

resp = urllib2.urlopen(request)
print resp.read()
