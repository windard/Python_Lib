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


# # coding=utf-8

# from lxml import etree

# html = etree.parse('test.html')
# result = etree.tostring(html)

# print result