#coding=utf-8

#加密：c = ( am + b )( mod 26 )
#解密：m = a(-1) ( c - b ) ( mod 26 )

moni = {'1':'1','3':'9','5':'21','7':'15','9':'3','11':'19','15':'7','17':'23','19':'11','21':'5','23':'17','25':'25'}
small_char = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
large_char = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def decypter(ciphertext,a=11,b=8):
    """
    affiner decypte
    usage: String , (int)a , (int)b
    """
    A = int(moni[str(a)])
    result = ""
    for i in ciphertext:
        if i in small_char:
            result += small_char[A*(small_char.index(i)-B)%26]
        else:
            result += large_char[A*(large_char.index(i)-B)%26]
    return result

def encrypter(plaintext,a=11,b=8):
    """
    affiner decypte
    usage : String , (int)a , (int)b
    """
    result = ""
    for i in plaintext:
        if i in small_char:
            result += small_char[(a*small_char.index(i)+b)%26]
        else:
            result += large_char[(a*large_char.index(i)+b)%26]
    return result
if __name__ == '__main__':
    # decypter("sjoyuxzr",11,8)
    # encrypter("sorcery",11,6)
