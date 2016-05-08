#coding=utf-8

#求最大公约数
def egcd(a,b):
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = egcd(b%a,a)
        return (g,x-(b//a)*y,y)

#求模逆
def moni(a,m):
    g,x,y = egcd(a,m)
    if g != 1:
        raise Exception("Modular Inverse Does Not Exist")
    else:
        return x % m

#欧拉函数，与一个数互素的数的个数
def euler(n):
    count = 0
    for x in xrange(0,n):
        g,x,y = egcd(x,n)
        if g == 1:
            count += 1
    return count
if __name__ == '__main__':
    print moni(19,26)
    print egcd(19,26)
    print euler(10)