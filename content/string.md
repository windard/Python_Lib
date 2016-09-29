## string

竟然到现在才找到这个标准库，真是不应该。

- whitespace -- a string containing all characters considered whitespace （空白字符）
- lowercase -- a string containing all characters considered lowercase letters （a-z）
- uppercase -- a string containing all characters considered uppercase letters （A-Z）
- letters -- a string containing all characters considered letters （a-zA-Z）
- digits -- a string containing all characters considered decimal digits （0-9）
- hexdigits -- a string containing all characters considered hexadecimal digits （0-9A-F）
- octdigits -- a string containing all characters considered octal digits （0-8）
- punctuation -- a string containing all characters considered punctuation （标点符号）
- printable -- a string containing all characters considered printable （可打印字符）

```
>>> string.whitespace
'\t\n\x0b\x0c\r '
>>> print string.whitespace




>>> print string.lowercase
abcdefghijklmnopqrstuvwxyz
>>> string.uppercase
'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
>>> string.letters
'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
>>> string.digits
'0123456789'
>>> string.hexdigits
'0123456789abcdefABCDEF'
>>> string.octdigits
'01234567'
>>> string.punctuation
'!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
>>> string.printable
'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c'
>>> print string.printable
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~




```
