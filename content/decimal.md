## decimal

一直觉得 python 很精确，相比于很多其他的语言，但是没想到吖，只是不曾遇到过，并不代表它精确。

这不是Python的问题，而是实数的无限精度跟计算机的有限内存之间的矛盾。

在 python 中的浮点数是 64 位的，而且可以自动的在整数和浮点数之间切换，非常的灵活，但是也无可奈何，根据 IEEE754 浮点数的规则，就是无法精确的表示所有的浮点数，具体可以查看 CSAPP 第二章。

无论你使用 python Java JavaScript PHP C 等任何编程语言，你都可以尝试一下输出 `0.1 + 0.2` 这个简单的计算，在 python 中它等于 `0.30000000000000004` , 而不是 `0.3` ，实际上，在其他编程语言中，也是这个值。

所以你会得到 `2.01 * 1000000 = 2009999.9999999998`, `2.1 * 100000000000000000000000 = 2.0999999999999998e+23` 等神奇的算式。

因为计算机只能使用二进制位表示数据，而这些浮点数除2为无限循环，所以只能舍弃精度来保存在计算机里，在使用的时候就会出现问题。

辛亏我们还有 decimal 库。

### 初步印象

python 中默认的是 17 位精度的小数，可以使用格式化字符串的方式获得更多位数，但是不精确，不过可以使用 decimal 获得 28 位甚至更多位数的精确小数。

```
In [1]: 1 / 3.0
Out[1]: 0.3333333333333333

In [2]: len('0.3333333333333333')
Out[2]: 18

In [3]: '%.30f' % (1 / 3.0)
Out[3]: '0.333333333333333314829616256247'

In [4]: len('0.333333333333333314829616256247')
Out[4]: 32

In [5]: import decimal

In [6]: decimal.getcontext
Out[6]: <function decimal.getcontext>

In [7]: decimal.getcontext()
Out[7]: Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999999, Emax=999999999, capitals=1, flags=[], traps=[DivisionByZero, Overflow, InvalidOperation])

In [8]: decimal.Decimal(1) / decimal.Decimal(3)
Out[8]: Decimal('0.3333333333333333333333333333')

In [9]: len('0.3333333333333333333333333333')
Out[9]: 30

In [10]: decimal.getcontext().prec = 50

In [11]: decimal.Decimal(1) / decimal.Decimal(3)
Out[11]: Decimal('0.33333333333333333333333333333333333333333333333333')

In [12]: len('0.33333333333333333333333333333333333333333333333333')
Out[12]: 52

In [13]: decimal.getcontext().prec = 100

In [14]: decimal.Decimal(1) / decimal.Decimal(3)
Out[14]: Decimal('0.3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')
```


### 实际使用

decimal 中可以更精确的表示和计算浮点数，就是比较麻烦的是，需要将浮点数用字符串的形式放入，不然还是那个不准的浮点数。

```
In [1]: from decimal import Decimal

In [2]: Decimal(2.1) * 1000000
Out[2]: Decimal('2100000.000000000088817841970')

In [3]: Decimal('2.1') * 1000000
Out[3]: Decimal('2100000.0')

In [4]: Decimal(2.01) * 1000000
Out[4]: Decimal('2009999.999999999786837179272')

In [5]: Decimal('2.01') * 1000000
Out[5]: Decimal('2010000.00')
```

或者是这样转换为以 `0.01` 为单位的小数

```
def monetize(decimal_num):
    if isinstance(decimal_num, decimal.Decimal):
        return decimal_num.quantize(decimal.Decimal('0.01'))
    else:
        return decimal.Decimal(decimal_num).quantize(
            decimal.Decimal('0.01'))

```

### 指定精度

一般的需求是 越精确越好，但是有的时候，过于精确反而会带来误差，还是适度比较好。

```
>>> from decimal import Decimal, getcontext
>>> Decimal(10042.3)*100000
Decimal('1004229999.999999927240423858')
>>> int(Decimal(10042.3)*100000)
1004229999
>>> getcontext().prec = 12
>>> int(Decimal(10042.3)*100000)
1004230000
```
