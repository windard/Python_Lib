# -*- coding: utf-8 -*-

import urllib

url = "http://techslides.com/demos/sample-videos/small.mp4"
filename = url.split('/')[-1]

download_name, headers = urllib.urlretrieve(url, filename)

print "filename: ", download_name
print "headers : "
print headers

urllib.urlcleanup()


resp = urllib.urlopen(url)
with open(filename, "w") as f:
    chunk = resp.read(1024)
    while chunk:
        f.write(chunk)
        chunk = resp.read(1024)

print "filename: ", filename
