# coding=utf-8

import os

basedir = os.getcwdu()
file_type = ['.py']

# coding=utf-8

import os
import codecs
import chardet
from docopt import docopt
import argparse

detail = False
basedir = os.getcwdu()
file_type = ['.py']


class LineCount(object):
    """
Line Count by Python , line can count code files and code lines.

Usage: 
  line [--type=<file>]
  line --verbose
  line (-h | --help)
  line (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  --verbose     Show detail.
  -t file, --type=<file>    Select file ext.
    """

    def __init__(self, root_dir=basedir, detail=False, file_type=file_type):
        self.root_dir = root_dir
        self.detail = detail
        self.file_num = 0
        self.line_num = 0
        self.file_type = file_type

    def find_file(self):
        """
        Count file num
        """
        for root, dirs, files in os.walk(self.root_dir):
            for filename in files:
                if os.path.splitext(filename)[1] in self.file_type:
                    self.file_num += 1
                    new_file_path = os.path.join(root, filename)
                    with open(new_file_path) as f:
                        comment = f.readline()
                        if comment == '# coding=utf-8\n' or comment == '# -*- coding: utf-8 -*-\n' or comment == '#coding=utf-8\n':
                            continue
                        f.seek(0)
                        page = f.read()
                    with open(new_file_path, 'w') as f:
                        f.seek(0)
                        f.write('# -*- coding: utf-8 -*-\n')
                        f.write(page)
                        print '['+new_file_path+']'
                    self.count_line(new_file_path)
                    fc = FileConvert(new_file_path, new_file_path)
                    fc.convert()

        print("Search in %-70s" % self.root_dir)
        print("file count: %d\nline count: %d" % (self.file_num, self.line_num))

    def count_line(self, filename):
        """
        Count file line
        """
        line_num = 0
        with open(filename, 'r') as f:
            while 1:
                data = f.readline()
                line_num += 1
                if not data:
                    break
        if self.detail:
            print('%-80s%d' % (filename, line_num))
        self.line_num += line_num


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
    def __init__(self, src, dest, origin='utf-8', final='utf-8', tabsize=4):
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
                single = line.replace('\r\n', '\n').replace('\t', ' '*self.tabsize)
                self.content.append(single)

    def write_file(self):

        with codecs.open(self.dest, 'wb', encoding=self.final) as f:
            for line in self.content:
                f.write(line.decode(self.origin))

    def convert(self):
        self.read_file()
        self.write_file()

if __name__ == '__main__':

    arguments = docopt(LineCount.__doc__, version='v1.0.0')

    if arguments['--verbose']:
        detail = True
    elif arguments['--type']:
        ext_file = arguments['--type']
        file_type = open(ext_file, 'r').read().split('\n')
    lc = LineCount(file_type=file_type, detail=detail)
    lc.find_file()
