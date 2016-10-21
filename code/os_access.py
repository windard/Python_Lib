# coding=utf-8

import os

print "File Name: ",__file__
print "Exist File ? ",os.access(__file__,os.F_OK)
print "Read File ? ",os.access(__file__,os.R_OK)
print "Write File ? ",os.access(__file__,os.W_OK)
print "Execute File ? ",os.access(__file__,os.X_OK)
