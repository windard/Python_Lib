# coding=utf-8

from functools import partial
from Tkinter import Tk,Button,X
from tkMessageBox import showinfo,showwarning,showerror

WARN = 'warn'
CRIT = 'crit'
REGU = 'regu'

SIGNS = {
	'do not enter:':CRIT,
	'railroad crossing':WARN,
	'55\nspeed limit':REGU,
	'wrong way':CRIT,
	'merging traffic':WARN,
	'one way':REGU,
}

critCB = lambda :showerror('Error','Error Button Pressed!')
warnCB = lambda :showwarning('Warning','Warning Button Pressed!')
infoCB = lambda :showinfo('Info','Info Button Pressed!')

top = Tk()
top.title('Road Signs')

Button(top,text='Quit',command=top.quit,bg='red',fg='white').pack()

MyButton = partial(Button,top)
CritButton = partial(MyButton,command=critCB,bg='white',fg='red')
WarnButton = partial(MyButton,command=warnCB,bg='goldenrod1')
ReguButton = partial(MyButton,command=infoCB,bg='white')

for eachSign in SIGNS:
	signType = SIGNS[eachSign]
	cmd = '%sButton(text=%r%s).pack(fill=X,expand=True)'%(signType.title(),eachSign,'.upper()' if signType==CRIT else '.title()')
	eval(cmd)

top.mainloop()