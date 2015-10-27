#coding=utf-8
import base64
old_decode =  "data to be encode"
encode = base64.b64encode(old_decode)
print encode
new_decode = base64.b64decode(encode)
print new_decode