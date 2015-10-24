import hashlib
decode = "data to be encode"
encode = hashlib.md5()
encode.update(decode)
print encode.hexdigest()