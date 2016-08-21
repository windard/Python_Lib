## SimpleHTTPServer

简单的 HTTP 服务器，使用 Python 只需要 4 行代码，不过只能执行 GET 请求。

```python
# coding=utf-8
# Written by Vamei
# Simple HTTPsERVER

import SocketServer
import SimpleHTTPServer

HOST = ''
PORT = 8001

# Create the server, SimpleHTTPRequestHander is pre-defined handler in SimpleHTTPServer package
server = SocketServer.TCPServer((HOST, PORT), SimpleHTTPServer.SimpleHTTPRequestHandler)
# Start the server
server.serve_forever()
```

功能同 `python -m SimpleHTTPServer 8001` , 默认端口为 8000

如果想要 POST 请求或者其他更多的高级功能，需要使用 CGIHTTPServer。