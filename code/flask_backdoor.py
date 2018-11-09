# -*- coding: utf-8 -*-
import signal
import time
from flask import Flask
from gevent import monkey
from gevent.backdoor import BackdoorServer


monkey.patch_all()

app = Flask(__name__)
def handle_backdoor(num, stack):
    server = BackdoorServer(('127.0.0.1', 4998))
    server.start()


signal.signal(signal.SIGUSR2, handle_backdoor)
now = time.ctime()

@app.route('/')
def index():
    global now
    now = time.ctime()
    return now


def main():
    app.run()


if __name__ == '__main__':
    main()
