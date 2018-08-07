## cProfile

性能检测工具

可以用来计算耗时

```
import cProfile
import re
cProfile.run('re.compile("foo|bar")')
```
