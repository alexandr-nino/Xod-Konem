#!/usr/bin/python
# -*- coding:u8 -*-
__author__ = '_killed_'

from PyQt4 import QtGui,QtCore

matrix = [
    (-1,-2),
    (-1,2),
    (1,-2),
    (1,2),
    (2,-1),
    (2,1),
    (-2,-1),
    (-2,1)
]


class MainWindow(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.resize(64*8,64*8)
        self.step=0

        self.started = False
        self.map = []
        for i in xrange(8):
            self.map.append([0 for x in xrange(8)])

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.calculate_steps)
        self.timer.start(300)
    # get next step
    def calculate_steps(self):
        if self.started:
            npx = None
            npy = None
            min = 9
            for x,y,s in self.get_weight(*self.pos):
                if self.step<63:
                    if 0<s<=min:
                        npx=x
                        npy=y
                        min=s
                else:
                    if s==0:
                        npx=x
                        npy=y
                        min=s
            self.step+=1
            self.pos = [npx,npy]
            self.map[npx][npy]=self.step

            if self.step ==64:
                self.timer.stop()

        self.repaint()
    # get array with [xpos,ypos,steps available]
    def get_weight(self,px,py):
        result = []
        for x,y in matrix:
            xx = x+px
            yy = y+py
            if 0<=xx<=7:
                if 0<=yy<=7:
                    if self.map[xx][yy] == 0:
                        cx = xx
                        cy = yy
                        steps = 0
                        for mx,my in matrix:
                            nx = mx+cx
                            ny = my+cy
                            if (0<=nx<=7) and (0<=ny<=7) and (self.map[nx][ny]==0):
                                steps+=1
                        result.append([xx,yy,steps])
                    else:
                        result.append([xx,yy,-1])

                else:
                    result.append([xx,yy,-1])
            else:
                result.append([xx,yy,-1])
        return result


    # change start point
    def mouseReleaseEvent(self, e):
        if not self.started:
            self.pos =[e.pos().x()/64,e.pos().y()/64]
            self.step+=1
            self.map[self.pos[0]][self.pos[1]]=self.step
            self.started = True



    # draw grid and steps
    def paintEvent(self, event):
        gc = QtGui.QPainter()
        gc.begin(self)
        # draw grid with black lines
        pen = QtGui.QPen(QtGui.QColor(0,0,0))
        gc.setPen(pen)
        for x in xrange(1,8):
            gc.drawLine(x*64,0,x*64,64*8)
            gc.drawLine(0,x*64,64*8,x*64)
        # draw steps
        for x in xrange(8):
            for y in xrange(8):
                if self.map[x][y] is not 0:
                    gc.drawText(x*64+30,y*64+30,str(self.map[x][y]))
        # end paint
        gc.end()

