#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'

from PyQt4 import QtGui,QtCore
from MWnd import MainWindow

class Application:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.wnd = MainWindow()
        self.wnd.show()
        self.app.exec_()

Application()



