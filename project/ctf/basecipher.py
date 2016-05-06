#coding=utf-8

def Basedecode(data,method="base64",flag=True):
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

if __name__ == '__main__':
    ans = Basedecode("Vm0wd1QyVkhVWGhVYmxKV1YwZDRXRmxVUm5kVlJscHpXa2M1VjFKdGVGWlZNbmhQWVd4YWMxZHViRmROYWxaeVdWZDRZV014WkhGU2JIQk9VbTVDZVZkV1pEUlRNazE0Vkc1T2FWSnVRazlWYWtwdlZWWmtWMWt6YUZSTlZUVkpWbTEwYzJGV1NuVlJiR2hYWWxSV1JGcFdXbXRXTVZwMFpFWlNUbFp1UWpaV2Fra3hVakZaZVZOcmJGSmlWR3hXVm01d1IyUldjRmhsUjBacVZtczFNVmt3WkRSVk1ERkZWbXBXVjFKc2NGaFdha3BIVTBaYWRWSnNTbGRTTTAwMQ==")
    # print "Result Is %s"%ans
