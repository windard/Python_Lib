# coding=utf-8

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

# 读取文本
text = open("./constitution.txt").read()

# 读取图片
alice_mask = np.array(Image.open('./alice_mask.jpg'))

# 设置禁词，不在词云中显示
stopwords = set(STOPWORDS)
stopwords.add("said")

# 生成词云，背景为白色，最多 2000 个词
wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask,
               stopwords=stopwords)
# generate word cloud
wc.generate(text)

# 保存图片
wc.to_file('alice.png')

# 第一幅，生成的词云
plt.imshow(wc)
plt.axis("off")
plt.figure()

# 第二幅，原图
plt.imshow(alice_mask, cmap=plt.cm.gray)
plt.axis("off")
plt.show()