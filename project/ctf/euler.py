#coding=utf-8


import time

def warp(func):
    def cost_time(*args, **kwargs):
        first = time.time()
        print first
        result = func(*args, **kwargs)
        sencode = time.time()
        print sencode
        print sencode - first
        return result
    return cost_time

class ElapsedTime(object):
    def __enter__(self):
        self.start_time = time.time()
        print self.start_time

    def __exit__(self, exception_type, exception_value, traceback):
        self.end_time = time.time()
        print self.end_time
        print "Speeds %d S."%(self.end_time - self.start_time)

#求最大公约数
def egcd(a,b):
    if a == 0:
        return (b,0,1)
    else:
        g,y,x = egcd(b%a,a)
        return (g,x-(b//a)*y,y)

@warp
def gcd(a, b):
    while b:
        a, b = b, a%b
    return a

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
    # print moni(19,26)
    # print egcd(19,26)
    # print euler(10)
    print gcd(23566354642335, 456567534545654)
    # with ElapsedTime():
        # print gcd(14345465685533465546684876857869756865365778, 3867745856879606978568674454754656745466486464577873564)