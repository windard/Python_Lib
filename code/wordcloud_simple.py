# coding=utf-8

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取文本
text = open("./constitution.txt").read()

# 生成词云
wordcloud = WordCloud().generate(text)

# 第一幅图，默认字体最大会达到屏幕宽度
plt.imshow(wordcloud)
plt.axis('off')

# 第二幅图，字体最大 40 px
wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")

# 显示
plt.show()

# 也可以使用 PIL 
# image = wordcloud.to_image()
# image.show()

# 显示结果保存为 'wordcloud.png'
wordcloud.to_file('wordcloud.png')