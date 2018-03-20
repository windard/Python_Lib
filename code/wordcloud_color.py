# coding=utf-8

from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# 读取文本
text = open("./constitution.txt").read()

# 读取图片
alice_coloring = np.array(Image.open('./pic1.jpg'))

# 设置禁词
stopwords = set(STOPWORDS)
stopwords.add("said")

# 生成词云
wc = WordCloud(background_color="white", 
               max_words=2000, 
               mask=alice_coloring,
               stopwords=stopwords, 
               max_font_size=20, 
               random_state=100)
# generate word cloud
wc.generate(text)


# 从图片中获得颜色
image_colors = ImageColorGenerator(alice_coloring)

# 第一幅 生成的词云
plt.imshow(wc)
plt.axis("off")
plt.figure()

# 第二幅 重新上色，与图片的颜色相近
plt.imshow(wc.recolor(color_func=image_colors))
plt.axis("off")
plt.figure()

# 第三幅 原图
plt.imshow(alice_coloring, cmap=plt.cm.gray)
plt.axis("off")
plt.show()