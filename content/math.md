##math

专用的数学计算的库，内置大量数学计算公式。                         

只列举了一些简单的可能常用的，还有很多，如果需要可以查看手册。             

```python
#coding=utf-8

import math

#e
print math.e

#π
print math.pi

pi = math.pi
p  = pi/2

#正弦
print math.sin(0)

#余弦
print math.cos(pi)

#正切
print math.tan(p)

#余切
# print 

#反正弦
print math.asin(0.5)

#反余弦
print math.acos(1)

#反正切
print math.atan(1)

#atan2(y,x) = atan(y/x)
print math.atan2(2,1)

#反余切


#双曲正弦
print math.sinh(0)

#双曲余弦
print math.cosh(1)

#双曲正切
print math.tanh(pi)

#双曲余切

#反双曲正弦
print math.asinh(0.5)

#反双曲余弦
print math.acosh(1)

#反双曲正切
print math.atanh(0.5)

#反双曲余切

#不小于的最小整数
print math.ceil(2.1)
print math.ceil(-2.1)

#不大于的最大整数
print math.floor(2.1)
print math.floor(-2.1)

#将数字转化为度数
print math.degrees(pi)

#将度数转化为数字
print math.radians(180)

#幂函数 同 e^x
print math.exp(1)

#幂函数结果减一 同 e^x -1  
print math.expm1(1)

#浮点数绝对值
print math.fabs(-10)

#阶乘
print math.factorial(5)

#浮点数求和
print math.fsum([1,2,3])

#勾股定理求弦 同 sqrt(x*x + y*y)
print math.hypot(3,4)

#判断浮点数是否无穷大 正无穷或者负无穷
print math.isinf(10000000)

#判断浮点数是否不是为一个数
print math.isnan(10.01)

#ldexp(x,i) = x * z**i
print math.ldexp(3,2)

#以e为底的指数函数
print math.log(1)

#以10为底的指数函数
print math.log10(100)

#以e为底的指数函数 但是参数为x+1
print math.log1p(0)

#乘方
print math.pow(2,4)

#开根号
print math.sqrt(9)
```

保存为math_demo.py，运行，看一下结果。                                

```python
2.71828182846
3.14159265359
0.0
-1.0
1.63312393532e+16
0.523598775598
0.0
0.785398163397
1.10714871779
0.0
1.54308063482
0.996272076221
0.48121182506
0.0
0.549306144334
3.0
-2.0
2.0
-3.0
180.0
3.14159265359
2.71828182846
1.71828182846
10.0
120
6.0
5.0
False
False
12.0
0.0
2.0
0.0
16.0
3.0
```
