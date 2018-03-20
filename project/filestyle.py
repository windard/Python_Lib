# coding=utf-8

import os
import codecs
import chardet
from docopt import docopt


class FileConvert(object):
    """
File Style by Python , detect your file character and change it to utf-8 and other things.

Usage:
  filestyle <src> <dest> [<origin>] [<final>] [<tabsize>]
  filestyle (-h | --help)
  filestyle (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.
    """
    def __init__(self, src, dest, origin='', final='utf-8', tabsize=4):
        self.src = src
        self.dest = dest
        self.origin = origin
        self.final = final
        self.tabsize = tabsize
        self.content = []

    def read_file(self):
        if not self.origin:
            self.origin = chardet.detect(open(self.src).read())['encoding']

        with codecs.open(self.src, 'rb', encoding=self.origin) as f:
            for line in f.xreadlines():
                single = line.replace('\r\n', '\n')
                self.content.append(single)

    def write_file(self):

        with codecs.open(self.dest, 'wb', encoding=self.final) as f:
            for line in self.content:
                f.write(line.decode(self.origin))

    def convert(self):
        self.read_file()
        self.write_file()


if __name__ == '__main__':
    arguments = docopt(FileConvert.__doc__, version='v1.0.0')

    src = arguments['<src>']
    dest = arguments['<dest>']
    origin = arguments.get('<origin>')
    final = arguments.get('<final>')
    if not final:
        final = 'utf-8'
    tabsize = arguments.get('<tabsize>', '4')
    if not tabsize:
        tabsize = '4'
    fc = FileConvert(src, dest, origin, final, int(tabsize))
    fc.convert()
