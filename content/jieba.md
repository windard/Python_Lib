## jieba

结巴，做最好的 Python 中文分词。

[Github 地址](https://github.com/fxsjy/jieba)

## 特点

- 支持三种分词模式
	- 精确模式，试图把句子最精确的分开，适合于文本分析
	- 全模式，把句子中所有的可以成词的词语都扫描出来，速度非常快，不能解决歧义
	- 搜索引擎模式，在精确模式的基础上，对长词再次切割，提高召回率，适合用于搜索引擎分词
- 支持繁体分词
- 支持自定义词典
- MIT 授权协议

## 算法

- 基于前缀词典实现高效的词图扫描，生成句子中汉子所有可能成词情况所构成的有向无环图（DAG）
- 采用了动态规划查找最大概率路径，找出基于词频的最大切分组合
- 对于未登录词，采用了基于汉字成词能力的 HMM 模型，采用了 Viterbi 算法

## 主要功能

### 分词

- `jieba.cut(self, sentence, cut_all=False, HMM=True)` 
	- `sentence` : 需要分词的字符串
	- `cut_all` : 是否采用全模式
	- `HMM` : 是否使用 HMM 模型

- `jieba.cut_for_search(self, sentence, HMM=True)`  用于搜索引擎构建倒排索引的分词，粒度比较细，即搜索引擎模式
	- `sentence` : 需要分词的字符串
	- `HMM` : 是否采用 HMM 模型

```
# encoding=utf-8
import jieba

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print("Search Mode:" + ", ".join(seg_list))
```

输出

```
λ python jieba_demo.py
Building prefix dict from the default dictionary ...
Loading model from cache c:\users\dell\appdata\local\temp\jieba.cache
Loading model cost 0.771 seconds.
Prefix dict has been built succesfully.
Full Mode: 我/ 来到/ 北京/ 清华/ 清华大学/ 华大/ 大学
Default Mode: 我/ 来到/ 北京/ 清华大学
他, 来到, 了, 网易, 杭研, 大厦
Search Mode:小明, 硕士, 毕业, 于, 中国, 科学, 学院, 科学院, 中国科学院, 计算, 计算所, ，, 后, 在, 日本, 京都,
大学, 日本京都大学, 深造
```

### 更改词典

`jieba.load_userdict(self, filename)`  载入自定义词典。词典格式；一个词占一行，一行分为三个部分：词语，词频（可省略），词性（可省略），用空格隔开，顺序不可颠倒，文件必须为 utf-8 编码。

`jieba.add_word(self, word, freq=None, tag=None)` 动态增加单词，三个参数分别为：词语，词频，词性。

`jiabe.del_word(self, word)` 动态删除单词。

`jieba.suggest_freq(self, segment, tune=False)` 动态刁杰词语的词频，使其能（或不能）被分出来


```
# coding=utf-8

import jieba

print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))

jieba.suggest_freq(('中', '将'), True)
print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))

print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))

jieba.suggest_freq('台中', True)
print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))

```

输出

```
λ python jieba_suggest.py
Building prefix dict from the default dictionary ...
Loading model from cache c:\users\dell\appdata\local\temp\jieba.cache
Loading model cost 0.827 seconds.
Prefix dict has been built succesfully.
如果/放到/post/中将/出错/。
如果/放到/post/中/将/出错/。
「/台/中/」/正确/应该/不会/被/切开
「/台中/」/正确/应该/不会/被/切开
```

### 关键词提取

`import jieba.analyse`

`jieba.analyse.extract_tags(self, sentence, topK=20, withWeight=False, allowPOS=(), withFlag=False)`
	- `sentence` : 待提取的文本
	- `topK` : 返回几个权重最大的关键词，默认为 20
	- `withWeight` : 是否一并返回关键词权重，默认为 False
	- `allowPOS` : 仅包括指定词性的词，默认为空，即不删选
	- `withFlag` : 当 allowPOS 非空的时候，True 即返回 单词和权重的原则，False 则仅返回单词

```
# coding=utf-8

import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser

USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)

content = open(file_name, 'rb').read()

tags = jieba.analyse.extract_tags(content, topK=topK)

print(",".join(tags))
``` 

提取许嵩的 《断桥残雪》 的歌词中的关键词

```
λ python jieba_extract.py bridge_snow.txt -k 10
Building prefix dict from the default dictionary ...
Loading model from cache c:\users\dell\appdata\local\temp\jieba.cache
Loading model cost 0.725 seconds.
Prefix dict has been built succesfully.
断桥,下过,寒月,编曲,融解,梅开,柳帘,独留,折翼,许嵩
```

### 词性标注

`jieba.posseg.POSTokenizer(tokenizer=None)` 新建分词器，可采用默认词性标注分词器。

```
# coding=utf-8

import jieba.posseg as posg

words = posg.cut("我爱北京天安门")

for word,flag in words:
	print("%s %s"%(word, flag))
```

输出

```
λ python jieba_cut.py
Building prefix dict from the default dictionary ...
Loading model from cache c:\users\dell\appdata\local\temp\jieba.cache
Loading model cost 0.784 seconds.
Prefix dict has been built succesfully.
我 r
爱 v
北京 ns
天安门 ns
```

### 并行分词

采用多进程并行分词，提高分词速度，使用 Python 自带的 multiprocess 库，暂不支持 Windows 

jieba.enable_parallel(4) # 开启并行分词模式，参数为并行进程数
jieba.disable_parallel() # 关闭并行分词模式

### 寻找词语在原文中的起始位置

`jieba.tokenize(self, unicode_sentence, mode=u'default', HMM=True)` 输入只接受 Unicode ,查找模式可选 `default` 默认模式或者 `search` 搜索模式。

```
# coding=utf-8

import jieba

print("Default Mode:")

result = jieba.tokenize(u'永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

print("Search Mode:")

result = jieba.tokenize(u'永和服装饰品有限公司', mode='search')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))
```

输出

```
λ python jieba_tokenize.py
Default Mode:
Building prefix dict from the default dictionary ...
Loading model from cache c:\users\dell\appdata\local\temp\jieba.cache
Loading model cost 0.718 seconds.
Prefix dict has been built succesfully.
word 永和                start: 0                end:2
word 服装                start: 2                end:4
word 饰品                start: 4                end:6
word 有限公司            start: 6                end:10
Search Mode:
word 永和                start: 0                end:2
word 服装                start: 2                end:4
word 饰品                start: 4                end:6
word 有限                start: 6                end:8
word 公司                start: 8                end:10
word 有限公司            start: 6                end:10
```