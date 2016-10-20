# coding=utf-8

import re
import sys
import unicodedata
from unidecode import unidecode

def slugify(value):
    if type(value) == unicode:
        value = unicode(unidecode(value))
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return  re.sub('[-\s]+', '-', value)

if __name__ == '__main__':
    print slugify(raw_input().decode(sys.stdin.encoding))
