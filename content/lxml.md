## lxml

试了这么多 HTML 解析库，好像都是这个的扩展，据说这个是解析速度最快的，那就来试一下的好了。

爬虫不仅仅只是爬虫，还是需要做一点东西出来的，做一个好一点的。数据分析，数据可视化，然后做一个漂亮的网站展示出来，这才是真正的一个完整的爬虫。

之前一直使用 BeautifulSoup 做内容解析，后来发现在爬到五千多页面的时候，BeautifulSoup 就会报错 `MemoryError` ,感觉还是用一些基础的库性能会更好一些，比如说用 urllib 取代 requests。

lxml 是一款高性能的 Python XML 解析库，因为它构建在两个 C 库上，执行效率惊人。

### 简单使用

```
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

result = etree.tostring(html)
print result

listresult = etree.tostringlist(html)
print listresult

unicoderesult = etree.tounicode(html)
print type(unicoderesult)

```

输出

```
<html><body><div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
         <br/>
     </li></ul>
 </div>
</body></html>
['<html><body><div>\n    <ul>\n         <li class="item-0"><a href="link1.html">first item</a></li>\n         <li class="item-1"><a href="link2.html">second item</a></li>\n         <li class="item-inactive"><a href="link3.html">third item</a></li>\n         <li class="item-1"><a href="link4.html">fourth item</a></li>\n         <li class="item-0"><a href="link5.html">fifth item</a>\n         <br/>\n     </li></ul>\n </div>\n</body></html>']
<type 'unicode'>
```

使用 lxml.etree 初始化 HTML 文本，会自动修正代码，可以看到帮我们补全了 li 标签，修正了 br 标签，添加了 html, body 标签。

我们也可以从文件中导入 HTML 代码

```
# coding=utf-8

from lxml import etree

html = etree.parse('test.html')
result = etree.tostring(html)

print result
```

与上文效果一致。

### 使用 xpath

在初始化 HTML 之后，就是使用 xpath 对 DOM 节点进行查找，虽然 xpath 是对 XML 文件进行查找的，但是对于 HTML 文件的解析也是一样没有问题的。

关于 xpath 解析可以查看 [阮一峰的: xpath 路径表达式笔记](http://www.ruanyifeng.com/blog/2009/07/xpath_path_expressions.html) [W3School: XPath 教程](http://www.w3school.com.cn/xpath/)

```
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

```

输出

```
['first item', 'second item', 'third item', 'fourth item', 'fifth item']
['link1.html', 'link2.html', 'link3.html', 'link4.html', 'link5.html']
['third item']
['item-0']
['fourth item']
[]
['item-0', 'item-1']
['first item', 'second item', 'third item', 'fourth item', 'fifth item']
['first item', 'link5.html']
```

