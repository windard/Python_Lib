## collections

collections 一个最重要的 类 就是计数器，妈妈再也不用担心我不会数数了。

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

# 输出排名前两名的字符
print cnt.most_common(2)
```