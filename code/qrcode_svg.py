# coding=utf-8

import qrcode
import qrcode.image.svg

def get_factory(method):
    if method == 'basic':
        # Simple factory, just a set of rects.
        factory = qrcode.image.svg.SvgImage
    elif method == 'fragment':
        # Fragment factory (also just a set of rects)
        factory = qrcode.image.svg.SvgFragmentImage
    else:
        # Combined path factory, fixes white space that may occur when zooming
        factory = qrcode.image.svg.SvgPathImage

def main():
    method = 'basic'
    factory = get_factory(method)
    img = qrcode.make('hello world', image_factory=factory)
    img.save("qrcode_svg.svg")


if __name__ == '__main__':
    main()
