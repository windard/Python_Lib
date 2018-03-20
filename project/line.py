# coding=utf-8

import os
from docopt import docopt
import argparse

detail = False
basedir = os.getcwdu()
file_type = ['.py', '.html', '.c', '.css', '.js', '.java', '.php', '.md', '.txt']


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
                    self.count_line(os.path.join(root, filename))

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


if __name__ == '__main__':

    arguments = docopt(LineCount.__doc__, version='v1.0.0')

    if arguments['--verbose']:
        detail = True
    elif arguments['--type']:
        ext_file = arguments['--type']
        file_type = open(ext_file, 'r').read().split('\n')
    lc = LineCount(file_type=file_type, detail=detail)
    lc.find_file()
