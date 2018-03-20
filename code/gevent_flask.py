# coding=utf-8

from flask import Flask
from gevent.pywsgi import WSGIServer


app = Flask(__name__)


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    http = WSGIServer(('', 5000), app)
    http.serve_forever()
