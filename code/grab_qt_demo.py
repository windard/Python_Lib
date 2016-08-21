#coding=utf-8

import sys  
from PyQt4.QtGui import QPixmap, QApplication  

app = QApplication(sys.argv)  
QPixmap.grabWindow(QApplication.desktop().winId()).save('grab_qt_demo.png', 'png')  