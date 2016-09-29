# coding=utf-8

from io import BytesIO

f = BytesIO()

f.write("This is test")
print f.getvalue()
