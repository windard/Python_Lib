## furl

URL 解析库 URLparse 的功能实在是令人吐槽，解析功能太烂就会有更好的来替代，这是自古以来的道理。所以来试一下 furl 吧，在下次遇到 URL 解析的时候也不要在 URLparse 在一头撞死。

```
>>> from furl import furl
>>> url="https://windard.com/2017/03/12/simple?name=windard&year=21#last"
>>> f = furl(url)
>>> f.scheme, f.host, f.port, f.path, f.query, f.fragment
('https', 'windard.com', 443, Path('/2017/03/12/simple'), Query('name=windard&year=21'), Fragment('last'))
>>> f.args
omdict1D([('name', 'windard'), ('year', '21')])
>>> f.args['name']
'windard'
>>> f.args['name'] = 'unknown'
>>> f
furl('https://windard.com/2017/03/12/simple?name=unknown&year=21#last')
>>> f.add('location=china')
furl('https://windard.com/2017/03/12/simple?name=unknown&year=21&location=china#last')
>>> f.set(scheme='http')
furl('http://windard.com/2017/03/12/simple?name=unknown&year=21&location=china#last')
```
