##operator

这是Python自带的函数库，操作符运算。                     
但是使用这个函数库的操作符比原生的操作符效率高,而且应用范围更大一些。                

```
#coding=utf-8

import operator

#加法
print operator.add(1,2)

#减法
print operator.sub(2,1)

#乘法
print operator.mul(4,5)

#除数取整 同a/b  
# / 可用于整数或浮点数
#浮点数即返回精确结果
print operator.div(9,4)
print operator.div(9.04,4)

#除数取整 同a//b 
#// 只能用于整数
#浮点数只能返回一位小数0
print operator.floordiv(9,4)
print operator.floordiv(9.04,4)

#除数取余 同a%b
print operator.mod(9,4)

#精确除法
print operator.truediv(9.04,4)

#绝对值
print operator.abs(-10)

#取反 相当于 -a
print operator.neg(-10)

#取反 相当于 ~a  
#~a = (-a)-1
#~10 = -11
#~(-10) = 9
print operator.inv(10)
print operator.inv(-10)
print operator.invert(10)
print operator.invert(-10)

#乘方 同a**b
print operator.pow(2,3)

#向左移位 同<< 相当于乘以2的相应次方
print operator.lshift(3,2)

#向右移位 同>> 相当于除以2的相应次方 取整
print operator.rshift(3,2)

#按位与 即 a&b
print operator.and_(1,8)
print operator.and_(1,1)

#按位或 即 a|b
print operator.or_(1,8)
print operator.or_(1,3)

#按位异或 即 a^b
print operator.xor(1,8)
print operator.xor(1,3)

#合并，不过只能用于序列
print operator.concat([1,2],[3,4])
print operator.concat(("one",),("two",))

#是否包含，同样是序列
print operator.contains([1,2,3],2)
print operator.contains([1,2,3],0)

#包含位置，同样是序列
print operator.indexOf([1,2,3],2)
#如果没有，则会抛出一个异常
# print operator.indexOf([1,2,3],0)

#包含 同 in
print operator.sequenceIncludes([1,2,3],1)
print operator.sequenceIncludes("123","1")

#计数,计算某个值在序列中出现的次数
print operator.countOf([1,2,1,3,1],1)
#set序列可以去重
print operator.countOf(set([1,2,1,3,1]),1)

#变量的值 同__index__()
a = 12
print operator.index(a)

#删除字典中的某对数值 同del a[b]
a = {0:"zero",1:"one",2:"two"}
operator.delitem(a,0)
print a

#删除序列中的某片数值 同del a[b:c]
a = [1,2,3,4,5]
operator.delslice(a,0,1)
print a

#取得字典的值 同 a[b]
a = {0:"zero",1:"one",2:"two"}
print operator.getitem(a,0)

#取得序列的片段 同 a[b:c]
a = [1,2,3,4,5]
print operator.getslice(a,0,2)

#设定字典的值 同 a[b]=c
a = {0:"zero",1:"one",2:"two"}
operator.setitem(a,3,"three")
print a

#设定序列的片段 同 a[b:c]=d
a = [1,2,3,4,5]
operator.setslice(a,1,2,["two"])
print a

#序列翻倍 同序列的 *=
a = [1,2,3]
print operator.repeat(a,5)
print operator.irepeat(a,5)

#判断值相等 同 =
print operator.eq(1,"1")
print operator.eq("a","a")

#判断值不等 同 !=
print operator.ne(1,"1")
print operator.ne("a","a")

#判断地址相等 同 is
print operator.is_(1,"1")
print operator.eq("a","a")

#判断地址不相等 同 is not
print operator.is_(1,"1")
print operator.eq("a","a")

#布尔值取反 同 not
print operator.not_(True)
print operator.not_(1==1)

#大于等于 >=
print operator.ge(5,5)
print operator.ge(5,9)

#大于 >
print operator.gt(5,5)
print operator.gt(5,0)

#大于等于 <=
print operator.le(5,5)
print operator.le(5,9)

##判断是否可调用
#在类的创建时是否使用使用__call__
#每一个函数都是可调用的
print operator.isCallable("abc")
print operator.isCallable(abs)

##判断是否是字典类型
print operator.isMappingType({1:"one",2:"two"})
print operator.isMappingType(1)

##判断是否是数字类型
print operator.isNumberType(1)
print operator.isNumberType(1.000001)

##判断是否是序列类型
print operator.isSequenceType([1,2,3])
print operator.isSequenceType((1,2,3))

#将与自身的值相加之和的值赋给自身 同 += 
#但是不改变自身的值，返回值返回相加的结果
a = 0
b = operator.iadd(a,2)
print a
print b

#将与自身序列相加的结果赋给自身 同 +=
#但是不改变自身的值，返回值返回相加的结果
a = [1,2]
b = [3,4]
c = operator.iconcat(a,b)
print c

#将与自身的值相减之和的值赋给自身 同 -= 
#但是不改变自身的值，返回值返回相减的结果
a = 2
b = operator.isub(a,1)
print a
print b

#将与自身的值相乘之和的值赋给自身 同 *= 
#但是不改变自身的值，返回值返回相乘的结果
a = 4
b = operator.imul(a,5)
print a
print b

#将与自身的值相除之和的值赋给自身 同 /= 
#这个除法是精确除法，不是取整
#但是不改变自身的值，返回值返回相除的结果
a = 9
b = operator.itruediv(a,2)
print a
print b

#将与自身的值相与的值赋给自身 同 &=
#但是不改变自身的值，返回值返回相与的结果
a = 8
b = operator.iand(a,1)
print a
print b

#将与自身的值相或的值赋给自身 同 |=
#但是不改变自身的值，返回值返回相或的结果
a = 8
b = operator.ior(a,1)
print a
print b

#将与自身的值相异或的值赋给自身 同 ^=
#但是不改变自身的值，返回值返回相异或的结果
a = 8
b = operator.ixor(a,1)
print a
print b

#将与自身相除取整的值赋给自身 同 /=
#但是不改变自身的值，返回值返回相除的结果
a = 9
b = operator.idiv(a,4)
print a
print b

#将与自身相除取整的值赋给自身 同 //=
#但是不改变自身的值，返回值返回相除的结果
a = 9.04
b = operator.ifloordiv(a,4)
print a
print b

#将与自身相移位的值赋给自身 同 <<=
#但是不改变自身的值，返回值返回移位的结果
a = 3
b = operator.ilshift(3,2)
print a
print b

#将与自身相移位的值赋给自身 同 >>=
#但是不改变自身的值，返回值返回移位的结果
a = 3
b = operator.irshift(3,2)
print a
print b

#同 +a
#并不知道有什么用
operator.pos(3)
```

保存为operator_demo.py，运行，看一下结果。                            

```python
3
1
20
2
2.26
2
2.0
1
2.26
10
10
-11
9
-11
9
8
12
0
0
1
9
3
9
2
[1, 2, 3, 4]
('one', 'two')
True
False
1
True
True
3
1
12
{1: 'one', 2: 'two'}
[2, 3, 4, 5]
zero
[1, 2]
{0: 'zero', 1: 'one', 2: 'two', 3: 'three'}
[1, 'two', 3, 4, 5]
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
False
True
True
False
False
True
False
True
False
False
True
True
True
False
False
True
True
True
False
True
True
False
True
True
True
True
0
2
[1, 2, 3, 4]
2
1
4
20
9
4.5
8
0
8
9
8
9
9
2
9.04
2.0
3
12
3
0
```