## ply

Python Lex-Yacc, 即 Python 版的 Lex-Yacc 工具，有了它们，你永远不需要自己手动写一个解析程序。

> 如果你在 `*nix` 电脑上，一般自带 Lex 和 Yacc ，try it youself .

### 前言

在很多年前，在大学上编译原理的时候，当时讲到编译流程，有什么词法生成树，句法生成树，抽象语法树什么之类的，再往后就没认真听了。

然后大作业是自己实现一个语法解析器，当时什么也不会，就知道什么遇到数字就继续读取，遇到符号就判断，可以循环判断和读取，用大量的 if,else 写了巨复杂的语法分析。

最近也在实现一个简单的输入规则分析，这次不是用 if,else 了，而是用的正则表达式，通过正则匹配获取结果。

其实在当时做大作业的时候，就已经有同学用 yacc 之类的分析工具，可以我到现在都不会用。

前段时间也用过 ast 抽象语法树之后，这一切终于都理顺了。

一段输入，首先需要被读取为字符串，（编码解码先不论），然后通过语法分析，（通过 if,else 判断，或者正则表达式解析，或者 yacc 这样的工具分析），然后生成抽象语法树，（这时已经生成对应的语法结构块），最后通过控制流程补充完善，得到执行对象。

## Lex&Yacc

Lex 和 Yacc 是什么？

Lex 和 Yacc 是一对好兄弟👬，一般搭配使用。Lex 是分词器，它用来根据规则对输入数据进行匹配操作。Yacc 是根据分词结果进行解析。

### Lex 示例

#### 开始的开始

lex_start.lt

```
%{
#include <stdio.h>
%}

%%
stop printf("Stop command received");
start printf("Start command reveived");
%%

```

这是我们的第一个 lex 代码，注意
1. 因为我们需要使用 `printf` 进行输出，引入了 `stdio.h` 库，学过 C 语言的同学应该对此很熟悉，使用 `%{` 和 `%}` 围起来的部分将原样导出，它们看起来并不对称。
2. 使用 `%%` 和 `%%` 围起来的段落，是我们的 lex 语法部分，第一句表示当输入流中读到 `stop` 时，执行 `printf("Stop command received");`, 第二句则是对 `start` 的操作。

使用 `lex lex_start.lt` 对其进行编译，将会生成 `lex.yy.c` 的 C 语言文件，然后使用 `cc lex.yy.c -o lex_start -ll` 生成可执行文件 `lex_start`

执行结果，当遇到 `start` 时，输出 `Start command reveived`,当遇到 `stop` 时，输出 `Stop command received`, 这里区分大小写，遇到其他值，则原样输出。输入多少，输出多少，只有大小写完全匹配 `start` 和 `stop` 的时候才会有不同的回应。

```
$ ./lex_start
start
Start command reveived
stop
Stop command received
yes
yes
no
no
!
!
^C
```

这里的 lex 更像一门 模板语言，可以引入 C 语言的一些功能，自己的主要功能是为了做匹配和操作。

#### 学一点正则

这些正则匹配规则都知道吧

```
[0123456789]+ 		# 表示一个或多个数字
[0-9]+ 				# 表示一个或多个数字
[a-z] 				# 表示单个a-z的字母
[a-z]* 				# 表示0个或多个字母
```

所以我们的正则匹配就开始了

lex_regex.lt

```
%{
#include <stdio.h>	
%}

%%
[0-9]+						printf("NUMBER\n");
[a-zA-Z][a-zA-Z0-9]*		printf("WORD\n");
%%

```

同样的编译运行查看结果。

```
$ lex lex_regex.lt
$ cc lex.yy.c -o lex_regex -ll
$ ./lex_regex
2334
NUMBER

dervr
WORD

str1
WORD

123avc
NUMBER
WORD

-12
-NUMBER

12.43
NUMBER
.NUMBER

a@a
WORD
@WORD

^C
```

看起来一切都很正常，数字和变量的定义都没问题.但是后面几个怎么看起来就不正常了，包括负数，小数，异常值。

#### 语法解析

虽然上面👆的词法解析有点小瑕疵，但是不影响，我们继续进行下一步语法解析。



[如何使用Lex/YACC](https://segmentfault.com/a/1190000000396608#articleHeader24)
