# -*- coding: utf-8 -*-

import string
import base64


base32_string = string.uppercase + "234567"

base64_string = string.uppercase + string.lowercase + string.digits + '+/'
base64_supply = [0, 2, 1]
base32_supply = [0, 2, 4, 1, 3]
base32_aside = [0, 6, 4, 3, 1]
base32_rest = [0, 3, 0, 1, 4, 0, 2]


def base64_encode(raw_string):
    bin_string = ''.join(map(lambda x: '{:08b}'.format(ord(x)),
                             raw_string.encode('utf-8')))
    length_left = len(raw_string) % 3
    bin_string += base64_supply[length_left] * "00"
    encode_string = ''.join([base64_string[int(bin_string[i:i+6], 2)]
                             for i in range(0, len(bin_string), 6)])
    return encode_string + base64_supply[length_left] * "="


def base64_decode(raw_string):
    bin_string = ''.join(map(lambda x: '{:06b}'.format(base64_string.index(x)),
                             raw_string.strip().replace("=", "")))
    length_right = raw_string.count("=")
    bin_string = bin_string[:-length_right*2] if length_right else bin_string
    return ''.join([chr(int(bin_string[i:i+8], 2))
                    for i in range(0, len(bin_string), 8)])


def base32_encode(raw_string):
    bin_string = ''.join(map(lambda x: '{:08b}'.format(ord(x)),
                             raw_string.encode('utf-8')))
    length_left = len(raw_string) % 5
    bin_string += base32_supply[length_left] * "0"
    encode_string = ''.join([base32_string[int(bin_string[i:i+5], 2)]
                             for i in range(0, len(bin_string), 5)])
    return encode_string + base32_aside[length_left] * "="


def base32_decode(raw_string):
    bin_string = ''.join(map(lambda x: '{:05b}'.format(base32_string.index(x)),
                             raw_string.strip().replace("=", "")))
    length_right = raw_string.count("=")
    bin_string = bin_string[:-base32_rest[length_right]] \
        if length_right else bin_string
    return ''.join([chr(int(bin_string[i:i+8], 2))
                    for i in range(0, len(bin_string), 8)])


def base16_encode(raw_string):
    return "".join(["{:X}".format(ord(i)) for i in raw_string.encode("utf-8")])


def base16_decode(raw_string):
    return "".join([chr(int(raw_string[i:i+2], 16))
                    for i in range(0, len(raw_string), 2)])


if __name__ == '__main__':
    print base64_encode("helloworld")
    print base64_encode("hello world")
    print base64_encode("hello  world")
    print base64_decode(base64_encode("helloworld"))
    print base64_decode(base64_encode("hello world"))
    print base64_decode(base64_encode("hello  world"))
    print base64.b64encode("helloworld")
    print base64.b64encode("hello world")
    print base64.b64encode("hello  world")

    print base32_encode("helloworld")
    print base32_encode("hello world")
    print base32_encode("hello  world")
    print base32_encode("hello   world")
    print base32_encode("hello    world")
    print base32_decode(base32_encode("helloworld"))
    print base32_decode(base32_encode("hello world"))
    print base32_decode(base32_encode("hello  world"))
    print base32_decode(base32_encode("hello   world"))
    print base32_decode(base32_encode("hello    world"))
    print base64.b32encode("helloworld")
    print base64.b32encode("hello world")
    print base64.b32encode("hello  world")
    print base64.b32encode("hello   world")
    print base64.b32encode("hello    world")

    print base16_encode("hello world")
    print base16_decode(base16_encode("hello world"))
