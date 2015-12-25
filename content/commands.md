##commands

这是一个专门用来执行shell的函数库，类似与os库的popen，它只有三个函数，非常简洁。                

1. commands.getoutput(cmd) 返回一个字符串，为cmd执行结果                             
2. commands.getstatusoutput(cmd) 返回一个元组，第一项为执行状态，第二项为执行结果                          
3. commands.getstatus(file) 返回一个字符串，为`ls -ld file`的执行结果                            

```python
>>> import commands
>>> result = commands.getoutput('ls')
>>> type(result)
<type 'str'>
>>> result
'code\ncontent\nothers\nproject\nREADME.md\ntest.md'
>>> print result
code
content
others
project
README.md
test.md
>>> result = commands.getoutput('ls -al')
>>> print result
total 36
drwxrwxr-x  7 windard windard 4096 12月 25 15:00 .
drwxrwxr-x 12 windard windard 4096 12月 15 19:43 ..
drwxrwxr-x  2 windard windard 4096 12月 25 14:34 code
drwxrwxr-x  3 windard windard 4096 12月 25 15:07 content
drwxrwxr-x  8 windard windard 4096 12月 23 01:26 .git
drwxrwxr-x  2 windard windard 4096 12月 15 19:59 others
drwxrwxr-x  2 windard windard 4096 12月 22 18:56 project
-rw-rw-r--  1 windard windard 2549 12月 25 14:49 README.md
-rw-rw-r--  1 windard windard   17 12月 25 15:00 test.md
>>> result = commands.getstatusoutput('ls')
>>> type(result)
<type 'tuple'>
>>> result[0]
0
>>> result[1]
'code\ncontent\nothers\nproject\nREADME.md\ntest.md'
>>> print result[1]
code
content
others
project
README.md
test.md
>>> result = commands.getstatusoutput('ls -ls')
>>> print result
(0, 'total 24\n4 drwxrwxr-x 2 windard windard 4096 12\xe6\x9c\x88 25 14:34 code\n4 drwxrwxr-x 3 windard windard 4096 12\xe6\x9c\x88 25 15:09 content\n4 drwxrwxr-x 2 windard windard 4096 12\xe6\x9c\x88 15 19:59 others\n4 drwxrwxr-x 2 windard windard 4096 12\xe6\x9c\x88 22 18:56 project\n4 -rw-rw-r-- 1 windard windard 2549 12\xe6\x9c\x88 25 14:49 README.md\n4 -rw-rw-r-- 1 windard windard   17 12\xe6\x9c\x88 25 15:00 test.md')
>>> print result[1]
total 24
4 drwxrwxr-x 2 windard windard 4096 12月 25 14:34 code
4 drwxrwxr-x 3 windard windard 4096 12月 25 15:09 content
4 drwxrwxr-x 2 windard windard 4096 12月 15 19:59 others
4 drwxrwxr-x 2 windard windard 4096 12月 22 18:56 project
4 -rw-rw-r-- 1 windard windard 2549 12月 25 14:49 README.md
4 -rw-rw-r-- 1 windard windard   17 12月 25 15:00 test.md
>>> result = commands.getstatus('test.md')
>>> type(result)
<type 'str'>
>>> result
'-rw-rw-r-- 1 windard windard 17 12\xe6\x9c\x88 25 15:00 test.md'
>>> print result
-rw-rw-r-- 1 windard windard 17 12月 25 15:00 test.md

```


