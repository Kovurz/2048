#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.initUI()

    def initUI(self):
        self.setStyle(QStyleFactory.create('fusion'))
        p=self.palette();
        p.setColor(QPalette.Window, QColor(120,120,130))
        p.setColor(QPalette.Button, QColor(53,53,53))
        p.setColor(QPalette.Highlight, QColor(142,45,197))
        p.setColor(QPalette.ButtonText, QColor(255,255,255))
        p.setColor(QPalette.WindowText, QColor(255,255,255))
        self.setPalette(p)

class Image(QLabel):
    def __init__(self,w,h,imgName):
        super().__init__()
        image = QPixmap(imgName)
        image = image.scaled(w,h,Qt.KeepAspectRatio)
        self.setPixmap(image)

class TextImg(QLabel):
    def __init__(self,txt):
        super().__init__()
        self.setText(txt)


class Block(QLabel):
    def __init__(self,num,x,y):
        super().__init__()
        self.block=QPixmap("mat.png")
        self.block=self.block.scaled(100,100,Qt.KeepAspectRatio)
        self.setPixmap(self.block)
        self.x=y
        self.y=x
        self.num=num
        self.setImage()

    def setImage(self):
        if self.num==2:
            self.image = QPixmap("atom.png")
        elif self.num==4:
            self.image=QPixmap("mat.png")
        elif self.num==8:
            self.image=QPixmap("terre.png")
        elif self.num==16:
            self.image=QPixmap("plaine.png")
        elif self.num==32:
            self.image=QPixmap("pays.png")
        elif self.num==64:
            self.image=QPixmap("continent.png")
        elif self.num==128:
            self.image=QPixmap("planete.png")
        elif self.num==256:
            self.image=QPixmap("solarSyst.png")
        elif self.num==512:
            self.image=QPixmap("galaxie.png")
        elif self.num==1024:
            self.image=QPixmap("amas.png")
        elif self.num==2048:
            self.image=QPixmap("univers.png")


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(590,610)
        self.setWindowTitle('2048 Space Version')
        self.setMenuBar()
        self.setCenter()
        self.availablegrille=range(16)
        self.blocks=[]
        self.initgrille(4,4)
        self.show()

    def setMenuBar(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('Fichier')
        helpMenu = mainMenu.addMenu('Aide')
        self.exitAction = QAction("&Quitter", self, icon=QIcon('exit.svg'), shortcut="Ctrl+Q", statusTip="Quitter l'application",triggered=self.quit)
        fileMenu.addAction(self.exitAction)
        self.newFile = QAction("&Nouvelle Partie", self,icon=QIcon('Reset.png'), statusTip="Nouvelle Partie",triggered=self.new)
        fileMenu.addAction(self.newFile)
        self.tuto = QAction('&Tutoriel',self,icon=QIcon('tuto.png'),shortcut="Ctrl+H",statusTip="Tutoriel",triggered=self.tuto)
        helpMenu.addAction(self.tuto)
        self.setCenter()
        self.show()

    def paintEvent(self,event):
        painter=QPainter(self)
        for b in self.blocks:
            painter.drawPixmap(QRect(b.x,b.y,100,100),b.image)

    def setCenter(self):
        qr= self.frameGeometry()
        cp= QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setBlock(self):
        a=random.randint(0,self.row-1)
        b=random.randint(0,self.col-1)
        while self.grille[a][b]!=1:
            a=random.randint(0,self.row-1)
            b=random.randint(0,self.col-1)
            #QApplication.processEvents()
        self.grille[a][b]=2
        self.updategrille()


    def initgrille(self,row,col):
        self.row=row
        self.col=col
        self.availablegrille=range(16)
        self.grille=[]
        for i in range(row):
            self.grille.append([])
            for j in range(col):
                self.grille[i].append(1)
        self.setBlock()
        self.setBlock()

    def up(self) :
        moved = False
        for i in range(4) :
            for j in range(4) :
                if self.grille[i][j] != 1 :
                    k = i
                    while k-1 >= 0 and self.grille[k-1][j] == 1 :
                        k -= 1
                    if k-1 >= 0 and self.grille[k-1][j] == self.grille[i][j] :
                        self.grille[k-1][j] *= 2
                        self.grille[i][j] = 1
                        moved = True
                    elif k < i :
                        self.grille[k][j] = self.grille[i][j]
                        self.grille[i][j] = 1
                        moved = True
        if moved :
            self.setBlock()


    def down(self) :
        moved = False
        for i in range(2,-1,-1) :
            for j in range(0,4) :
                if self.grille[i][j] != 1 :
                    k = i
                    while k+1 < 4 and self.grille[k+1][j] == 1 :
                        k += 1
                    if k+1 < 4 and self.grille[k+1][j] == self.grille[i][j] :
                        self.grille[k+1][j] *= 2
                        self.grille[i][j] = 1
                        moved = True
                    elif k > i :
                        self.grille[k][j] = self.grille[i][j]
                        self.grille[i][j] = 1
                        moved = True
        if moved :
            self.setBlock()


    def left(self) :
        moved = False
        for i in range(4) :
            for j in range(4) :
                if self.grille[i][j] != 1 :
                    k = j
                    while k-1 >= 0 and self.grille[i][k-1] == 1 :
                        k -= 1
                    if k-1 >= 0 and self.grille[i][k-1] == self.grille[i][j] :
                        self.grille[i][k-1] *= 2
                        self.grille[i][j] = 1
                        moved = True
                    elif k < j :
                        self.grille[i][k] = self.grille[i][j]
                        self.grille[i][j] = 1
                        moved=True
        if moved :
            self.setBlock()

    def right(self) :
        moved = False
        for i in range(0,4) :
            for j in range(2,-1,-1) :
                if self.grille[i][j] != 1 :
                    k = j
                    while k+1 < 4 and self.grille[i][k+1] == 1 :
                        k += 1
                    if k+1 < 4 and self.grille[i][k+1] == self.grille[i][j] :
                        self.grille[i][k+1] *= 2
                        self.grille[i][j] = 1
                        moved = True
                    elif k > j :
                        self.grille[i][k] = self.grille[i][j]
                        self.grille[i][j] = 1
                        moved = True

        if moved :
            self.setBlock()


    def updategrille(self) :
        self.blocks=[]
        self.availablegrille = []
        for i in range(4) :
            for j in range(4) :
                if self.grille[i][j] != 1 :
                    self.blocks.append(Block(self.grille[i][j],i*self.width()/4+30,j*self.height()/4+10))
                    self.availablegrille.append(i+j*4)
        if not self.movesAvailable() :
            self.gameOver()
        self.win()
        self.update()

    def movesAvailable(self) :
        for i in range(4) :
            for j in range(4) :
                if self.grille[i][j]==1:
                    return True
                if i < 3 and self.grille[i][j] == self.grille[i+1][j] :
                    return True
                if j < 3 and self.grille[i][j] == self.grille[i][j+1] :
                    return True
        return False


    def gameOver(self):
        dialog=QMessageBox(self)
        dialog.setText("T'AS PERDU, tu veux rejouer ? :)")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        if dialog.exec_()==QMessageBox.Ok:
            self.new()
        else:
            self.close()

    def win(self) :
        for i in range(4) :
            for j in range(4) :
                if self.grille[i][j] == 2048 :
                    if QMessageBox.question(self,'Message',"<center><b>Congratulation !</b><br>Recommencer ?</center>",QMessageBox.Ok,QMessageBox.Cancel)==QMessageBox.Ok:
                        self.new()
                    else:
                        self.close()

    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Space:
            self.new()
        elif e.key() == Qt.Key_Up :
            self.blocks=[]
            self.up()
        elif e.key() == Qt.Key_Down :
            self.blocks=[]
            self.down()
        elif e.key() == Qt.Key_Left :
            self.blocks=[]
            self.left()
        elif e.key() == Qt.Key_Right :
            self.blocks=[]
            self.right()
        self.movesAvailable()
        self.updategrille()
        self.update()

    def quit(self):
        dialog = QMessageBox(self)
        dialog.setText("Souhaitez-vous quitter l'application ?")
        dialog.setIcon(QMessageBox.Question)
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Ok)
        if dialog.exec_()==QMessageBox.Ok:
            QCoreApplication.instance().quit()

    def new(self):
        self.initgrille(4,4)
        self.updategrille()


    def tuto(self):
        fen = QDialog(self)
        layout= QGridLayout()
        w= 50
        h= 50
        atom = Image(w,h,"atom.png")
        mat =  Image(w,h,"mat.png")
        terre =  Image(w,h,"terre.png")
        plaine =  Image(w,h,"plaine.png")
        pays =  Image(w,h,"pays.png")
        continent=  Image(w,h,"continent.png")
        planete =  Image(w,h,"planete.png")
        solar =  Image(w,h,"solarSyst.png")
        galaxie =  Image(w,h,"galaxie.png")
        amas =  Image(w,h,"amas.png")
        univers =  Image(w,h,"univers.png")
        atom1 = TextImg("Atom:")
        mat1 = TextImg("Matière organique:")
        terre1 = TextImg("Terre:")
        plaine1 =  TextImg("Plaine:")
        pays1 = TextImg("Pays:")
        continent1= TextImg("Continent:")
        planete1 = TextImg("Planète:")
        solar1 =  TextImg("Système solaire:")
        galaxie1 =  TextImg("Galaxie:")
        amas1 = TextImg("Amas de galaxie:")
        univers1 =  TextImg("Univers:")
        layout.addWidget(atom,0,1)
        layout.addWidget(mat,1,1)
        layout.addWidget(terre,2,1)
        layout.addWidget(plaine,3,1)
        layout.addWidget(planete,6,1)
        layout.addWidget(solar,7,1)
        layout.addWidget(galaxie,8,1)
        layout.addWidget(amas,9,1)
        layout.addWidget(univers,10,1)
        layout.addWidget(pays,4,1)
        layout.addWidget(continent,5,1)
        layout.addWidget(atom1,0,0)
        layout.addWidget(mat1,1,0)
        layout.addWidget(terre1,2,0)
        layout.addWidget(plaine1,3,0)
        layout.addWidget(solar1,7,0)
        layout.addWidget(galaxie1,8,0)
        layout.addWidget(amas1,9,0)
        layout.addWidget(univers1,10,0)
        layout.addWidget(pays1,4,0)
        layout.addWidget(continent1,5,0)
        layout.addWidget(planete1,6,0)

        fen.setLayout(layout)
        fen.setWindowTitle('Tutoriel')
        fen.show()

app = Application([])
win = Window()
app.exec_()
