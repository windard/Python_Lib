#coding=utf-8

from M2Crypto import RSA,BIO

rsa = RSA.gen_key(2048, 3, lambda *agr:None)
pub_bio = BIO.MemoryBuffer()
priv_bio = BIO.MemoryBuffer()

rsa.save_pub_key_bio(pub_bio)
rsa.save_key_bio(priv_bio, None)

pub_key = RSA.load_pub_key_bio(pub_bio)
priv_key = RSA.load_key_bio(priv_bio)

message = 'HHNDrCSpvBVPyMFpkrxCrU0xRYjFdHqv'

encrypted = pub_key.public_encrypt(message, RSA.pkcs1_padding).encode("base64").replace("\n","")
decrypted = priv_key.private_decrypt(encrypted.decode("base64"), RSA.pkcs1_padding)

print str(len(encrypted.replace("\n","")))+encrypted
print decrypted

# CwihCsz/uFwnkGZzpxfXfeS57rlkwsZHyl5DFmdFu4WuTRKShZGR+hSOTMkxHh9iXPnc/pcstJbB5ovo0q2HhJj/K9ZJoWxYE9Zb0H7gPAYjrWPH9xwKKXKycOPcbU35uxGJvrdeB6+2jdUBZBkVkGVyTPIQCe17CTCvBVI4DYRLk0Uu3IVoFkl9F9MiJvHGTTCmT5PgOezwXYHF/0BihHTiWjpUqlh50AWVYkkhlw6mV2hSlw84N7NM35HaeQLG4HAirEjKRECWe0d+0NIjtS5zTFEuK5TEbgEUJTfi9WbUncYZ+hpm28nvKspKBf3DprGh2/7hIOtxVmaTnNRwXw==
