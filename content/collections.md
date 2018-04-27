## collections

### 计数器

collections 一个重要的 类 就是计数器，妈妈再也不用担心我不会数数了。

小时候我们数数是这样数的

```
# coding=utf-8

words = ['a', 'b', 'c', 'b', 'a', 'a', 'b', 'c']

cnt = {}

for word in words:
	if word in cnt:
		cnt[word] += 1
	else:
		cnt[word] = 1

print cnt

```

现在我们可这样数数

```
# coding=utf-8

words = ['a', 'b', 'c', 'b', 'a', 'a', 'b', 'c']

from collections import Counter

cnt = Counter(words)

# 输出全部排名
print cnt

# 输出排名前两名的字符
print cnt.most_common(2)
```

其实使用原生列表也是可以的，像这样

```
# coding=utf-8

words = ['a', 'b', 'c', 'b', 'a', 'a', 'b', 'c']

count = {}

for key in set(words):
    count[key] = words.count(key)

print count

```

还可以使用其进行统计文件

```
# coding=utf-8


from collections import Counter

with open('filename', 'rb') as f:
    line_count = Counter(f)
print(line_count)

```

### 字典

一般的字典进行赋值操作时，需要先检查键是否存在，`defaultdict` 则不需要

> 使用 defaultdict 的时候需注意，初始化的时候需要填入想要的值的类型。

```
# coding=utf-8

from collections import defaultdict

colours = (
    ('Yasoob', 'Yellow'),
    ('Ali', 'Blue'),
    ('Arham', 'Green'),
    ('Ali', 'Black'),
    ('Yasoob', 'Red'),
    ('Ahmed', 'Silver'),
)

favourite_colours = defaultdict(list)

for name, colour in colours:
    favourite_colours[name].append(colour)

print(favourite_colours)

```

除了可以对字典直接进行赋值之外，还可以对字典进行嵌套赋值

```
# 异常输出：KeyError: 'colours'
some_dict = {}
some_dict['colours']['favourite'] = "yellow"

```

直接进行嵌套赋值

```
import collections
tree = lambda: collections.defaultdict(tree)
some_dict = tree()
some_dict['colours']['favourite'] = "yellow"
```

### 双端队列

在 Python 内置函数库 Queue 中已经提供了队列和栈， 在这里提供了双端队列 deque ,可以两边插入，两边取出。

```
# coding=utf-8

from collections import deque

d = deque()

d.append(1)
d.append(2)
d.appendleft(3)
d.appendleft(4)

print d

print d.pop()
print d.popleft()

print d[0]
print d[-1]

```

输出

```
deque([4, 3, 1, 2])
2
4
3
1
```

还可以限制队列长度，超出长度的数据会被另一端挤出, 还可以进行队列的循环移位，左移或右移

```
# coding=utf-8

from collections import deque

l = deque(maxlen=5)
l.extend(range(5))

print l, len(l)

l.extendleft([6])

print l, len(l)

l.rotate(2)
print l

l.rotate(-3)
print l

l.reverse()
print l

```

输出

```
deque([0, 1, 2, 3, 4], maxlen=5) 5
deque([6, 0, 1, 2, 3], maxlen=5) 5
deque([2, 3, 6, 0, 1], maxlen=5)
deque([0, 1, 2, 3, 6], maxlen=5)
deque([6, 3, 2, 1, 0], maxlen=5)
```

### 有序字典

字典是无序的，输入与输出的顺序都不一定一样, collections 中的 OrderedDict 能保证输出输入顺序绝对一致

```
# coding=utf-8

from collections import OrderedDict

d = {}
d[1] = 'one'
d[3] = 'three'
d[2] = 'two'

print d

o = OrderedDict()

o[1] = 'one'
o[3] = 'three'
o[2] = 'two'

print o

```

### 字典元组

元组是一个不可变列表，可以通过索引来查找元组中的元素。

namedtuple 是一个字典类型的元组，同样是不可变的，但是它又和字典一样存在键值对。

```
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

```

### 枚举类型

枚举对象在 Python 中也有一个库 `enum` ， 枚举类型(Enums) 是一种组织各种东西的方式。

但是在 collections 库中，只有在 Python 3.4 及以上才能够使用 Enum 枚举类型

```
# coding=utf-8

from collections import namedtuple
from enum import Enum


class Species(Enum):
    cat = 1
    dog = 2
    horse = 3
    aardvark = 4
    butterfly = 5
    owl = 6
    platypus = 7
    dragon = 8
    unicorn = 9
    # 依次类推

    # 但我们并不想关心同一物种的年龄，所以我们可以使用一个别名
    kitten = 1  # (译者注：幼小的猫咪)
    puppy = 2   # (译者注：幼小的狗狗)

Animal = namedtuple('Animal', 'name age type')
perry = Animal(name="Perry", age=31, type=Species.cat)
drogon = Animal(name="Drogon", age=4, type=Species.dragon)
tom = Animal(name="Tom", age=75, type=Species.cat)
charlie = Animal(name="Charlie", age=2, type=Species.kitten)

print charlie.type == tom.type
print charlie.type
print tom.type

# 虽然所有的 cat 类型被 kitten 类型覆盖，但是仍然可以使用 cat
print Species(1)
print Species['cat']
print Species.cat

```
