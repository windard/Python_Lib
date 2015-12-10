##额外的东西

1. python自带了一个简单web的服务器，当前目录下启动,就可以在`localhost:8080`查看。
```python
python -m SimpleHTTPServer 8080
```

2. PHP 5.4版本及以上也自带了一个简单的web服务器，在当前目录下启动，就可以在`localhost:8000`查看。
```php
php -S localhost:8000
```

3. 最简单的nodejs的服务器。
```javascript
var http = require('http');
http.createServer(function (req, res) {
    res.send('Hello');
    res.end();
}).listen(3000);
```
保存为server.js,在当前目录下cmd里输入`node server.js`即可调用，在`localhost:3000`查看。
