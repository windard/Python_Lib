import md5
decode = "data to be encode"
encode = md5.new()
encode.update(decode)
print encode.hexdigest()