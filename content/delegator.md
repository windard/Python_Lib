## delegator

命令执行库，和 subprocess 类似,其实底层使用的就是 subprocess

```
# coding=utf-8

from delegator import run


def system_has_pbcopy():
    process = run("which pbcopy", block=True)
    return process.return_code == 0


def subprocess_system_has_pbcopy():
    p = subprocess.Popen(["which", "pbcopy"], stdout=subprocess.PIPE)
    return p.wait() == 0


if __name__ == '__main__':
    print system_has_pbcopy()
    print subprocess_system_has_pbcopy()

```
