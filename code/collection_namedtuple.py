# coding=utf-8

from collections import namedtuple

Animal = namedtuple('Animal', 'name age type')
perry = Animal(name="perry", age=31, type="cat")

print perry

print perry.name

# 仍然可以继续使用索引
print perry[0]

# 还可以将其转换为字典
print perry._asdict
