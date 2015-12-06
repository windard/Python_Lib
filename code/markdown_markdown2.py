#coding=utf-8

import markdown2

data = """
##这是markdown测试文档
-----

####我们需要一个小标题

1. 有序列表
2. 有序列表
2. 不那么有序的有序列表

- 无序的
- 无序的

>这是一段引用的话
>对，引用还没完

```python
This is code block
hello world
```


	or like This
	this is python 
	hello python


- [] 未完成的任务一
- [] 未完成的任务二
- [x] 已完成的任务三

**At Last ** You Can [Click Here](http://simple.wenqiangyang.com) To Find Me

"""

result = markdown2.markdown(data.decode("utf-8"))

print result