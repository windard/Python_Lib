import hashlib
decode = "data to be encode"
encode = hashlib.sha1()
encode.update(decode)
print encode.hexdigest()