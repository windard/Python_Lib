#coding=utf-8

def Caesardecode(data,flag=True):
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
    # ans = Caesardecode("Jr1p0zr2VfPp")