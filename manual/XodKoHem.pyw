#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = 'Alex'
from PyQt4 import QtGui,QtCore
class Step:
    positon = []
    num = 0
    def __init__(self,pos,num=0):
        self.position = pos
        self.num = num
class MainWindow(QtGui.QMainWindow):
    map = [[0,0,0,0,0,0,0,0] for i in xrange(8)] #Matrix 8x8
    position = None
    arr=[]
    def __init__(self):
        super(MainWindow,self).__init__()
        self.resize(32*8+200,32*8)
        self.setWindowTitle(self.trUtf8("Ход Конем"))

        self.tb = QtGui.QTextBrowser(self)
        self.tb.move(32*8,0)
        self.tb.resize(200,32*8)

        doc_string = QtCore.QString(""" система подсказок отображает число возможных ходов из поля в которое можно сходить.
по правилу Варндсфора для успешного прохождения следует выбирать поле с наименьшим числов ходов,
если  таких полей несколько выбирается любое.
        """)

        self.tb.setText(self.trUtf8(doc_string))



        self.timer = QtCore.QTimer(self)
        self.connect(self.timer,QtCore.SIGNAL("timeout()"),self.repaint)
        self.timer.setInterval(50)
        self.timer.start()

    def Calculator(self):
        steps = [[2,1],[2,-1],
                [-2,1],[-2,-1],
                [1,2],[-1,2],
                [1,-2],[-1,-2]
            ] # Matrix2x8
        self.arr = []
        steps_arr = []
        for i in steps:
            newpos = [self.position[0]+i[0],self.position[1]+i[1]]
            if 0<=newpos[0]<=7 and 0<=newpos[1]<=7:
                if self.map[newpos[0]][newpos[1]] != 1:
                    steps_arr.append( Step(newpos) )
        for i in steps_arr:
            for ii in steps:
                newpos = [i.position[0]+ii[0],i.position[1]+ii[1]]
                if 0<=newpos[0]<=7 and 0<=newpos[1]<=7:
                    if self.map[newpos[0]][newpos[1]] != 1:
                        i.num+=1
        self.arr = steps_arr[:]
        del steps_arr[:]

    def mouseReleaseEvent(self, QEvent):
        p= QEvent.pos()
        x = p.x()/32
        y = p.y()/32

        if self.map[x][y]==0:
            self.position = [x,y]
            if self.map[x][y] == 0:
                self.map[x][y]=1

        
        self.Calculator()
    def paintEvent(self, *args, **kwargs):
        
        gc = QtGui.QPainter()
        gc.begin(self)
        
        self.drawGreed(gc)
        self.drawMap(gc)
        
        gc.end()
    def drawGreed(self,gc):
        
        gc.setPen(QtGui.QColor("black"))

        for x in xrange(0,8*32,32):
            gc.drawLine(0,x,32*8,x)
            gc.drawLine(x,0,x,32*8)
    def drawMap(self,gc):

        if self.arr is not []:
            for i in self.arr:
                x,y = i.position
                if i.num <= 1:
                    gc.setPen(QtGui.QColor("green"))
                else:
                    c=str(hex(0x0+32*i.num))[2:]
                    gc.setPen(QtGui.QColor(eval("0x{0}{0}{0}".format(c))))
                gc.drawEllipse(x*32+1,y*32+1,30,30)
                gc.setPen(QtGui.QColor("black"))
                gc.drawText(x*32+15,y*32+20,str(i.num))
        gc.setPen(QtGui.QColor("red"))
        for x in xrange(8):
            for y in xrange(8):
                if self.map[x][y] is 1:
                    gc.drawEllipse(x*32+1,y*32+1,30,30)

app = QtGui.QApplication([])
w=MainWindow()
w.show()
app.exec_()