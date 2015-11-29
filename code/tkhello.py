#coding=utf-8

import Tkinter

#此处是为大写的T和小写的Y
top = Tkinter.Tk()

hello = Tkinter.Label(top,text="hello,world!")
hello.pack()

quit = Tkinter.Button(top,text="QUIT",command=top.quit,bg='red',fg='white')
quit.pack(fill=Tkinter.X,expand=1)
#quit.pack()
Tkinter.mainloop()





