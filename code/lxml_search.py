# coding=utf-8

from lxml import etree

text = """
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
         <br>
     </ul>
 </div>
"""

html = etree.HTML(text)

# 查找所有的 li 标签下的 a 标签 的内容
result = html.xpath("//li/a/text()")
print result

# 查找所有的 li 标签下的 a 标签 的连接
result = html.xpath("//li/a/@href")
print result

# 查找 class 为 item-inactive 下的 a 标签的内容
result = html.xpath("//li[@class='item-inactive']/a/text()")
print result

# 查找 最后一个 li 标签的 class
result = html.xpath("//li[last()]/@class")
print result

# 查找 倒数第二个 li 标签下的子节点
result = html.xpath("//li[last()-1]/node()")
print result[0].xpath("text()")

# 查找 第二个 li 标签的内容
result = html.xpath("//li[2]/text()")
print result

# 查找 前两个 li 标签的 class
result = html.xpath("//li[position()<3]/@class")
print result

# 查找所有 带有 href 的节点
result = html.xpath("//*[@href]/text()")
print result

# 从根节点查找所有元素节点
result = html.xpath("/*")
print result[0].xpath("body/div/ul/li[1]/a/text()|body/div/ul/li[last()]/a/@href")
