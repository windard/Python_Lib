# coding=utf-8

words = ['a', 'b', 'c', 'b', 'a', 'a', 'b', 'c']

cnt = {}

for word in words:
	if word in cnt:
		cnt[word] += 1
	else:
		cnt[word] = 1

print cnt

from collections import Counter

cnt = Counter(words)

# 输出排名前两名的字符
print cnt.most_common(2)