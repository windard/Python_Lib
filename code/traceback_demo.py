# coding=utf-8
import traceback
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    traceback.print_stack()
    return 'hello world'


def main():
    app.run()


if __name__ == '__main__':
    main()
