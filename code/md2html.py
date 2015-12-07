#coding=utf-8
import markdown
import codecs

p = codecs.open("markdown.html","r","utf-8")
d = p.read()
p.close()

r = markdown.markdown(d)

l = codecs.open("markdown2.html","w","utf-8")
l.write(r)
l.close()