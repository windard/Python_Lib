#coding=utf-8

from colorama import init,Fore

init(autoreset=True)
#通过使用autoreset参数可以让变色效果只对当前输出起作用，输出完成后颜色恢复默认设置
print(Fore.RED + 'This is red color')
print('automatically back to default color again')
