#
#    peepdf is a tool to analyse and modify PDF files
#    http://peepdf.eternal-todo.com
#    By Jose Miguel Esparza <jesparza AT eternal-todo.com>
#
#    Copyright (C) 2014 Jose Miguel Esparza
#
#    This file is part of peepdf.
#
#        peepdf is free software: you can redistribute it and/or modify
#        it under the terms of the GNU General Public License as published by
#        the Free Software Foundation, either version 3 of the License, or
#        (at your option) any later version.
#
#        peepdf is distributed in the hope that it will be useful,
#        but WITHOUT ANY WARRANTY; without even the implied warranty of
#        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
#        GNU General Public License for more details.
#
#        You should have received a copy of the GNU General Public License
#        along with peepdf.    If not, see <http://www.gnu.org/licenses/>.
#

# Python version of the jjdecode function written by Syed Zainudeen
# http://csc.cs.utm.my/syed/images/files/jjdecode/jjdecode.html
# +NCR/CRC! [ReVeRsEr] - crackinglandia@gmail.com
#
# The original algorithm was written in Javascript by Yosuke Hasegawa (http://utf-8.jp/public/jjencode.html)
#
# Modified to integrate it with peepdf

# Add JJencoder by crackinglandia (https://github.com/crackinglandia/python-jjencode/blob/master/jjencode.py)
# and changed a little to his code
#
# Modified by Windard 5.10 2016

import re
from struct import unpack

class JJEncoder(object):
    """
    usage: JJEncoder(text, var_name = "$", palindrome = False).encode()
    """

    def __init__(self, text, var_name = "$", palindrome = False):
        self.encoded_text = self.__encode(var_name, text)

        if palindrome:
            self.encoded_text = re.split("[,;]$", self.encoded_text)[0]
            self.encoded_text = """\"\'\\\"+\'+\",""" + self.encoded_text + "".join(list(self.encoded_text)[::-1])

    def __encode(self, gv, text):
        r = ""
        n = None
        t = None
        b = [ "___", "__$", "_$_", "_$$", "$__", "$_$", "$$_", "$$$", "$___", "$__$", "$_$_", "$_$$", "$$__", "$$_$", "$$$_", "$$$$"]
        s = ""

        for i in range(len(text)):
            n = ord(text[i])
            if (n == 0x22 or n == 0x5c):
                 s += "\\\\\\" + chr(unpack("b", text[i])[0])
            elif ((0x21 <= n and n <= 0x2f) or (0x3A <= n and n <= 0x40) or ( 0x5b <= n and n <= 0x60 ) or ( 0x7b <= n and n <= 0x7f)):
                s += text[i]

            elif ((0x30 <= n and n <= 0x39) or (0x61 <= n and n <= 0x66)):
                if s:
                    r += '"' + s + '"+'

                if n < 0x40:
                    tmp_index = n - 0x30
                else:
                    tmp_index = n - 0x57

                r += gv + "." + b[ tmp_index ] + "+"
                s = ""

            elif n == 0x6c: # 'l'
                if s:
                    r += '"' + s + '"+'

                r += '(![]+"")[' + gv + '._$_]+'
                s = ""

            elif n == 0x6f: # 'o'
                if s:
                    r += '"' + s + '"+'

                r += gv + "._$+"
                s = ""
            elif n == 0x74: # 'u'
                if s:
                    r += '"' + s + '"+'

                r += gv + ".__+"
                s = ""
            elif n == 0x75: # 'u'
                if s:
                    r += '"' + s + '"+'

                r += gv + "._+"
                s = ""
            elif n < 128:
                if s:
                    r += '"' + s
                else:
                    r += '"'

                r += '\\\\"+' + "".join([self.__f(gv, b, i) for i in [int(x) for x in re.findall("[0-7]", oct(n))[1:]]])
                s = ""
            else:
                if s:
                    r += '"' + s
                else:
                    r += '"'

                r += '\\\\"+' + gv + "._+" + "".join([self.__g(gv, b, i) for i in [int(x) for x in re.findall("[0-9a-f]", oct(n), re.I)[1:]]])
                s = ""

        if s:
            r += '"' + s + '"+'

        r = (gv + "=~[];" +
        gv + "={___:++" + gv +',$$$$:(![]+"")['+gv+"],__$:++"+gv+',$_$_:(![]+"")['+gv+"],_$_:++"+
        gv+',$_$$:({}+"")['+gv+"],$$_$:("+gv+"["+gv+"""]+"")["""+gv+"],_$$:++"+gv+',$$$_:(!""+"")['+
        gv+"],$__:++"+gv+",$_$:++"+gv+',$$__:({}+"")['+gv+"],$$_:++"+gv+",$$$:++"+gv+",$___:++"+gv+",$__$:++"+gv+"};"+
        gv+".$_="+
        "("+gv+".$_="+gv+'+"")['+gv+".$_$]+"+
        "("+gv+"._$="+gv+".$_["+gv+".__$])+"+
        "("+gv+".$$=("+gv+'.$+"")['+gv+".__$])+"+
        "((!"+gv+')+"")['+gv+"._$$]+"+
        "("+gv+".__="+gv+".$_["+gv+".$$_])+"+
        "("+gv+'.$=(!""+"")['+gv+".__$])+"+
        "("+gv+'._=(!""+"")['+gv+"._$_])+"+
        gv+".$_["+gv+".$_$]+"+
        gv+".__+"+
        gv+"._$+"+
        gv+".$;"+
        gv+".$$="+
        gv+".$+"+
        '(!""+"")['+gv+"._$$]+"+
        gv+".__+"+
        gv+"._+"+
        gv+".$+"+
        gv+".$$;"+
        gv+".$=("+gv+".___)["+gv+".$_]["+gv+".$_];"+
        gv+".$("+gv+".$("+gv+'.$$+"\\""+' + r + '"\\"")())();')

        return r

    def __f(self, a, b, c):
        return a + "." + b[c] + "+"

    def __g(self, a, b, c):
        return a + "." + b[int(c, 16)] + "+"

    def encode():
        return encoded_text

class JJDecoder(object):
    """
    usage: JJDecoder(text).decode()
    """

    def __init__(self, jj_encoded_data):
        self.encoded_str = jj_encoded_data

    def clean(self):
        self.encoded_str = re.sub('^\s+|\s+$', '', self.encoded_str)

    def checkPalindrome(self):
        startpos = -1
        endpos = -1
        gv, gvl = -1, -1

        index = self.encoded_str.find('"\'\\"+\'+",')

        if index == 0:
            startpos = self.encoded_str.find('$$+"\\""+') + 8
            endpos = self.encoded_str.find('"\\"")())()')
            gv = self.encoded_str[index + 9:self.encoded_str.find('=~[]')]
            gvl = len(gv)
        else:
            gv = self.encoded_str[0:self.encoded_str.find('=')]
            gvl = len(gv)
            startpos = self.encoded_str.find('"\\""+') + 5
            endpos = self.encoded_str.find('"\\"")())()')

        return (startpos, endpos, gv, gvl)

    def decode(self):

        self.clean()
        startpos, endpos, gv, gvl = self.checkPalindrome()

        if startpos == endpos:
            return (-1, 'There is no data to decode')

        data = self.encoded_str[startpos:endpos]

        b = ['___+', '__$+', '_$_+', '_$$+', '$__+', '$_$+', '$$_+', '$$$+', '$___+', '$__$+', '$_$_+', '$_$$+',
             '$$__+', '$$_$+', '$$$_+', '$$$$+']

        str_l = '(![]+"")[' + gv + '._$_]+'
        str_o = gv + '._$+'
        str_t = gv + '.__+'
        str_u = gv + '._+'

        str_hex = gv + '.'

        str_s = '"'
        gvsig = gv + '.'

        str_quote = '\\\\\\"'
        str_slash = '\\\\\\\\'

        str_lower = '\\\\"+'
        str_upper = '\\\\"+' + gv + '._+'

        str_end = '"+'

        out = ''
        while data != '':
            # l o t u
            if data.find(str_l) == 0:
                data = data[len(str_l):]
                out += 'l'
                continue
            elif data.find(str_o) == 0:
                data = data[len(str_o):]
                out += 'o'
                continue
            elif data.find(str_t) == 0:
                data = data[len(str_t):]
                out += 't'
                continue
            elif data.find(str_u) == 0:
                data = data[len(str_u):]
                out += 'u'
                continue

            # 0123456789abcdef
            if data.find(str_hex) == 0:
                data = data[len(str_hex):]

                for i in range(len(b)):
                    if data.find(b[i]) == 0:
                        data = data[len(b[i]):]
                        out += '%x' % i
                        break
                continue

            # start of s block
            if data.find(str_s) == 0:
                data = data[len(str_s):]

                # check if "R
                if data.find(str_upper) == 0:  # r4 n >= 128
                    data = data[len(str_upper):]  # skip sig
                    ch_str = ''
                    for i in range(2):  # shouldn't be more than 2 hex chars
                        # gv + "."+b[ c ]
                        if data.find(gvsig) == 0:
                            data = data[len(gvsig):]
                            for k in range(len(b)):  # for every entry in b
                                if data.find(b[k]) == 0:
                                    data = data[len(b[k]):]
                                    ch_str = '%x' % k
                                    break
                        else:
                            break

                    out += chr(int(ch_str, 16))
                    continue

                elif data.find(str_lower) == 0:  # r3 check if "R // n < 128
                    data = data[len(str_lower):]  # skip sig

                    ch_str = ''
                    ch_lotux = ''
                    temp = ''
                    b_checkR1 = 0
                    for j in range(3):  # shouldn't be more than 3 octal chars
                        if j > 1:  # lotu check
                            if data.find(str_l) == 0:
                                data = data[len(str_l):]
                                ch_lotux = 'l'
                                break
                            elif data.find(str_o) == 0:
                                data = data[len(str_o):]
                                ch_lotux = 'o'
                                break
                            elif data.find(str_t) == 0:
                                data = data[len(str_t):]
                                ch_lotux = 't'
                                break
                            elif data.find(str_u) == 0:
                                data = data[len(str_u):]
                                ch_lotux = 'u'
                                break

                        # gv + "."+b[ c ]
                        if data.find(gvsig) == 0:
                            temp = data[len(gvsig):]
                            for k in range(8):  # for every entry in b octal
                                if temp.find(b[k]) == 0:
                                    if int(ch_str + str(k), 8) > 128:
                                        b_checkR1 = 1
                                        break

                                    ch_str += str(k)
                                    data = data[len(gvsig):]  # skip gvsig
                                    data = data[len(b[k]):]
                                    break

                            if b_checkR1 == 1:
                                if data.find(str_hex) == 0:  # 0123456789abcdef
                                    data = data[len(str_hex):]
                                    # check every element of hex decode string for a match
                                    for i in range(len(b)):
                                        if data.find(b[i]) == 0:
                                            data = data[len(b[i]):]
                                            ch_lotux = '%x' % i
                                            break
                                    break
                        else:
                            break

                    out += chr(int(ch_str, 8)) + ch_lotux
                    continue

                else:  # "S ----> "SR or "S+
                    # if there is, loop s until R 0r +
                    # if there is no matching s block, throw error

                    match = 0;
                    n = None

                    # searching for matching pure s block
                    while True:
                        n = ord(data[0])
                        if data.find(str_quote) == 0:
                            data = data[len(str_quote):]
                            out += '"'
                            match += 1
                            continue
                        elif data.find(str_slash) == 0:
                            data = data[len(str_slash):]
                            out += '\\'
                            match += 1
                            continue
                        elif data.find(str_end) == 0:  # reached end off S block ? +
                            if match == 0:
                                return (-1, '+ No match S block')
                            data = data[len(str_end):]
                            break  # step out of the while loop
                        elif data.find(str_upper) == 0:  # r4 reached end off S block ? - check if "R n >= 128z
                            if match == 0:
                                return (-1, 'No match S block n>128')
                            data = data[len(str_upper):]  # skip sig

                            ch_str = ''
                            ch_lotux = ''

                            for j in range(10):  # shouldn't be more than 10 hex chars
                                if j > 1:  # lotu check
                                    if data.find(str_l) == 0:
                                        data = data[len(str_l):]
                                        ch_lotux = 'l'
                                        break
                                    elif data.find(str_o) == 0:
                                        data = data[len(str_o):]
                                        ch_lotux = 'o'
                                        break
                                    elif data.find(str_t) == 0:
                                        data = data[len(str_t):]
                                        ch_lotux = 't'
                                        break
                                    elif data.find(str_u) == 0:
                                        data = data[len(str_u):]
                                        ch_lotux = 'u'
                                        break

                                # gv + "."+b[ c ]
                                if data.find(gvsig) == 0:
                                    data = data[len(gvsig):]  # skip gvsig
                                    for k in range(len(b)):  # for every entry in b
                                        if data.find(b[k]) == 0:
                                            data = data[len(b[k]):]
                                            ch_str += '%x' % k
                                            break
                                else:
                                    break  # done
                            out += chr(int(ch_str, 16))
                            break  # step out of the while loop
                        elif data.find(str_lower) == 0:  # r3 check if "R // n < 128
                            if match == 0:
                                return (-1, 'No match S block n<128!!')

                            data = data[len(str_lower):]  # skip sig

                            ch_str = ''
                            ch_lotux = ''
                            temp = ''
                            b_checkR1 = 0

                            for j in range(3):  # shouldn't be more than 3 octal chars
                                if j > 1:  # lotu check
                                    if data.find(str_l) == 0:
                                        data = data[len(str_l):]
                                        ch_lotux = 'l'
                                        break
                                    elif data.find(str_o) == 0:
                                        data = data[len(str_o):]
                                        ch_lotux = 'o'
                                        break
                                    elif data.find(str_t) == 0:
                                        data = data[len(str_t):]
                                        ch_lotux = 't'
                                        break
                                    elif data.find(str_u) == 0:
                                        data = data[len(str_u):]
                                        ch_lotux = 'u'
                                        break

                                # gv + "."+b[ c ]
                                if data.find(gvsig) == 0:
                                    temp = data[len(gvsig):]
                                    for k in range(8):  # for every entry in b octal
                                        if temp.find(b[k]) == 0:
                                            if int(ch_str + str(k), 8) > 128:
                                                b_checkR1 = 1
                                                break

                                            ch_str += str(k)
                                            data = data[len(gvsig):]  # skip gvsig
                                            data = data[len(b[k]):]
                                            break

                                    if b_checkR1 == 1:
                                        if data.find(str_hex) == 0:  # 0123456789abcdef
                                            data = data[len(str_hex):]
                                            # check every element of hex decode string for a match
                                            for i in range(len(b)):
                                                if data.find(b[i]) == 0:
                                                    data = data[len(b[i]):]
                                                    ch_lotux = '%x' % i
                                                    break
                                else:
                                    break
                            out += chr(int(ch_str, 8)) + ch_lotux
                            break  # step out of the while loop
                        elif (0x21 <= n and n <= 0x2f) or (0x3A <= n and n <= 0x40) or (0x5b <= n and n <= 0x60) or (
                                0x7b <= n and n <= 0x7f):
                            out += data[0]
                            data = data[1:]
                            match += 1
                    continue
            return (-1, 'No match in the code!!')
            break
        return (0, out)


if __name__ == '__main__':
    # j = JJEncoder('alert("Hello, JavaScript" )')
    # print j.encode()
    data = open("JJ.txt","r").read()
    j = JJDecoder(data)
    print j.decode()