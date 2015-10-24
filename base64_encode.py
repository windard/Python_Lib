old_decode =  "data to be encode"
encode = old_decode.encode("base64")
print encode
new_decode = encode.decode("base64")
print new_decode