# coding=utf-8

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取文本
text = open("./bridge_snow.txt").read()

# 中文分词，然后用空格连接起来
text = " ".join(jieba.cut(text))

# 生成词云
wordcloud = WordCloud(font_path='./msyh.ttc').generate(text)

# 第一幅图，默认字体最大会达到屏幕宽度
plt.imshow(wordcloud)
plt.axis('off')

# 显示
plt.show()
