# coding=utf-8

import Tkinter 

top = Tkinter.Tk()

label = Tkinter.Label(top,text="Hello World")
label.pack()

quit = Tkinter.Button(top,text="Quit",command=top.quit)
quit.pack()

Tkinter.mainloop()