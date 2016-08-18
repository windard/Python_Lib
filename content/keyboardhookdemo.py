#coding=utf-8

import pyHook,pythoncom

def onKeyboardEvent(event):
	print "MessageName:",event.MessageName
	print "Message:",event.Message
	print "Time:",event.Time
	print "Window:",event.Window
	print "WindowName",event.WindowName
	print "Ascii:",event.Ascii,chr(event.Ascii)
	print "Key:",event.Key
	print "KeyID:",event.KeyID
	print "ScanCode:",event.ScanCode
	print "Extended:",event.Extended
	print "Injected:",event.Injected
	print "Alt",event.Alt
	print "Transition:",event.Transition

	return True

hm = pyHook.HookManager()
hm.KeyDown = onKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()
