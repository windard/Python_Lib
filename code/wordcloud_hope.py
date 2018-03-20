# coding=utf-8

import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import random

from wordcloud import WordCloud, STOPWORDS, random_color_func

# 自定义灰色主色调
def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

# 读取文本
text = open("./a_new_hope.txt").read()

# 读取图片
mask = np.array(Image.open('./stormtrooper_mask.png'))

# preprocessing the text a little bit
text = text.replace("HAN", "Han")
text = text.replace("LUKE'S", "Luke")

# adding movie script specific stopwords
stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

wc = WordCloud(max_words=1000, 
               mask=mask, 
               stopwords=stopwords, 
               margin=10,
               random_state=1).generate(text)
# store default colored image
default_colors = wc.to_array()

# 第一幅 自定义颜色
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
wc.to_file("a_new_hope.png")
plt.axis("off")
plt.figure()

# 第二幅 随机颜色
plt.title("Random colors")
plt.imshow(wc.recolor(color_func=random_color_func, random_state=3))
plt.axis("off")
plt.figure()

# 第二幅 默认颜色
plt.title("Default colors")
plt.imshow(default_colors)
plt.axis("off")
plt.show()