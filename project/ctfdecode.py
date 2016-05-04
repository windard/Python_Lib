#coding=utf-8

def Basedecode(data,method,flag):
    """
    decode Base encoded data
    usage: String Method True|False
    Method : base64 , base32 , base16
    True : show each results
    False : Just show result
    """
    try:
        num = 0
        if flag:
            print "Num %4d : %s"%(num,data)
        while 1:
            data = data.decode(method)
            num += 1
            if flag:
                print "Num %3d : %s"%(num,data)
    except Exception, e:
        return data

def Caesardecode(data,flag):
    """
    decode Caesar encode data
    usage : String True:False
    True : show each result
    False : resturn all results
    """
    results = []
    for j in range(0,27):
        result = ""
        for i in data:
            if ord(i) > ord('A') and ord(i) < ord('Z'):
                if ord(i)+j > ord('Z'):
                    result += chr((ord(i)+j)%ord('Z')+ord('A')-1)
                else:
                    result += chr(ord(i)+j)
            elif ord(i) > ord('a') and ord(i) < ord('z'):
                if ord(i)+j > ord('z'):
                    result += chr((ord(i)+j)%ord('z')+ord('a')-1)
                else:
                    result += chr(ord(i)+j)
            else:
                result += i
        results.append(result)
        if flag:
            print "Num %3d : %s"%(j,result)
    if not flag:
        return results

if __name__ == '__main__':
    # ans = Basedecode("Vm0wd1QyVkhVWGhVYmxKV1YwZDRXRmxVUm5kVlJscHpXa2M1VjFKdGVGWlZNbmhQWVd4YWMxZHViRmROYWxaeVdWZDRZV014WkhGU2JIQk9VbTVDZVZkV1pEUlRNazE0Vkc1T2FWSnVRazlWYWtwdlZWWmtWMWt6YUZSTlZUVkpWbTEwYzJGV1NuVlJiR2hYWWxSV1JGcFdXbXRXTVZwMFpFWlNUbFp1UWpaV2Fra3hVakZaZVZOcmJGSmlWR3hXVm01d1IyUldjRmhsUjBacVZtczFNVmt3WkRSVk1ERkZWbXBXVjFKc2NGaFdha3BIVTBaYWRWSnNTbGRTTTAwMQ==","base64",True)
    # print "Result Is %s"%ans

    # ans = Caesardecode("Jr1p0zr2VfPp",False)
    # for i in ans:
    #     if "we" in i or "We" in i:
    #         print i

