## qrcode

qrcode 二维码生成库

### 命令行使用

```
> qr -h
Usage: qr - Convert stdin (or the first argument) to a QR Code.

When stdout is a tty the QR Code is printed to the terminal and when stdout is
a pipe to a file an image is written. The default image format is PNG.

Options:
  -h, --help            show this help message and exit
  --factory=FACTORY     Full python path to the image factory class to create
                        the image with. You can use the following shortcuts to
                        the built-in image factory classes: pil, pymaging,
                        svg, svg-fragment, svg-path.
  --optimize=OPTIMIZE   Optimize the data by looking for chunks of at least
                        this many characters that could use a more efficient
                        encoding method. Use 0 to turn off chunk optimization.
  --error-correction=ERROR_CORRECTION
                        The error correction level to use. Choices are L (7%),
                        M (15%, default), Q (25%), and H (30%).
> qr "hello world"
█████████████████████████████
█████████████████████████████
████ ▄▄▄▄▄ ██▄▀▄▄█ ▄▄▄▄▄ ████
████ █   █ █   ▄▀█ █   █ ████
████ █▄▄▄█ █ █▄▀▄█ █▄▄▄█ ████
████▄▄▄▄▄▄▄█ █ █▄█▄▄▄▄▄▄▄████
████▄▀ ▄  ▄▀█ █ ▀▀     █▀████
████ █ █▄ ▄▄█ ▄▀  ▄█▀  ▄█████
███████▄█▄▄▄ ▄▀█ ▄▄█▀▀██ ████
████ ▄▄▄▄▄ █▀██▄█▀▄▀█▀  ▀████
████ █   █ █ ▀█▄▀▀  ▀▀██▄████
████ █▄▄▄█ █▄ ▀█ ▀█▄▀▀ ██████
████▄▄▄▄▄▄▄█▄▄█▄▄█▄█▄██▄█████
█████████████████████████████
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

也可以导出到图片，默认是 png 格式，也可以导出为 svg 格式

```
> qr 'Hello world' > test.png
> qr --factory=svg "hello world">test.svg
```

### 一般用法

```
# coding=utf-8

import qrcode

img = qrcode.make("hello world")
img.save("test.png")

```


### 高级使用

```
# coding=utf-8

import qrcode

qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data('this is a new qrcode')

qr.print_ascii()
qr.print_tty()


img = qr.make_image()
img.show()
img.save('qrcode_high.png')

```

- version: 表示二维码的版本号，二维码总共有1到40个版本，最小的版本号是1，对应的尺寸是21×21，每增加一个版本会增加4个尺寸。这里说的尺寸不是只生成图片的大小，而是指二维码的长宽被平均分为多少份。
- error_correction: 指的是纠错容量，这就是为什么二维码上面放一个小图标也能扫出来，纠错容量有四个级别，分别是
  - ERROR_CORRECT_L L级别，7%或更少的错误能修正
  - ERROR_CORRECT_M M级别，15%或更少的错误能修正，也是qrcode的默认级别
  - ERROR_CORRECT_Q Q级别，25%或更少的错误能修正
  - ERROR_CORRECT_H H级别，30%或更少的错误能修正
- box_size: 用来控制二维码的每个单元(box)格有多少像素点
- border: 表示二维码的边框宽度，4是最小值，也是默认值

生成矢量图的方法

```
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

```