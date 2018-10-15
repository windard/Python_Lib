# -*- coding: utf-8 -*-
import signal
import pdb
from flask import Flask

app = Flask(__name__)
signal.signal(signal.SIGUSR2, lambda num,stack: pdb.set_trace())


@app.route('/')
def index():
    return json.dumps({"name":"windard"})


def main():
    app.run()


if __name__ == '__main__':
    data = json.dumps({"name":"windard"})
    main()
