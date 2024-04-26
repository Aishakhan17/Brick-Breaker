from PySide6.QtWidgets import *
from PySide6 import QtCore, QtGui
from PySide6.QtGui import *
from PySide6.QtCore import *
import sys, random, time, math

class MainWindowDis(QWidget):
    def __init__(self):
        super(MainWindowDis,self).__init__()
        self.setWindowTitle("Brick Breaker")
        self.windowWidth = 1000
        self.windowHeight = 600
        self.setFixedSize(self.windowWidth,self.windowHeight)
        self.layout = QGridLayout()
        self.layout.setEnabled(True)
        self.setLayout(self.layout)
        self.paddle = drawPaddle()
        self.layout.addChildWidget(self.paddle)
        self.paddleMoveEvent()
        self.ball = drawBall()
        self.layout.addChildWidget(self.ball)
        self.uiComponents()
        self.brickGrid()
        self.show()

    def uiComponents(self):
        self.ball.move(490,555)
        self.paddle.move(425,575)

        
    def paddleMoveEvent(self):
        QShortcut(QKeySequence(Qt.Key_Left),self,activated = self.paddleMoveLeft)
        QShortcut(QKeySequence(Qt.Key_Right),self,activated = self.paddleMoveRight)
    
    def paddleMoveLeft(self): 
        self.paddleDist = QPoint(70,0)
        self.paddleCurrentPos = self.paddle.pos()
        if self.paddleCurrentPos.x() >=25:
            self.newPaddlePos = self.paddleCurrentPos - self.paddleDist
            self.paddle.move(self.newPaddlePos)
    
    def paddleMoveRight(self):        
        self.paddleDist = QPoint(70,0)
        self.paddleCurrentPos = self.paddle.pos()       
        if self.paddleCurrentPos.x() <=830:
            self.newPaddlePos = self.paddleCurrentPos + self.paddleDist
            self.paddle.move(self.newPaddlePos)

    def brickGrid(self):
        global row_length, row_width
        row_length = 14
        row_width = 7
        self.gridList = []
        x = 70
        y = 35
        for i in range(row_length):
            self.temp_grid = []
            for j in range(row_width):
                self.brick = drawBrick()
                self.layout.addChildWidget(self.brick)
                self.temp_grid.append(self.brick)
            self.gridList.append(self.temp_grid)

        for i in range(row_length):
            for j in range(row_width):
                self.gridList[i][j].setGeometry(x*i+10,y*j+10,x,y)

    
class drawPaddle(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(160,30)
        self.paintEvent(QPaintEvent)
    
    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(0.5,0.5)
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor(Qt.black))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QColor("#FF8000"))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        prect = QRect(3, 2, 150, 20)
        painter.drawRoundedRect(prect,10,10)
        painter.end()
        
class drawBall(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(22,22)
        self.paintEvent(QPaintEvent)


    def paintEvent(self, QPaintEvent):
        painter = QPainter(self)
        painter.translate(0.5,0.5)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(Qt.black))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QColor("#1E1E1E"))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        circ = QRect(0,0,20,20)
        painter.drawEllipse(circ)
        painter.end()

class drawBrick(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(65,30)
        
    def paintEvent(self, QPaintEvent):
        colors = ["#a52a2a","#ff8c00","#2f4f4f","#4b0082"]
        painter = QPainter(self)
        painter.translate(0.5,0.5)
        pen = QPen()
        pen.setWidth(3)
        pen.setColor(QColor(Qt.black))
        painter.setPen(pen)

        brush = QtGui.QBrush()
        brush.setColor(QColor(random.choice(colors)))
        brush.setStyle(Qt.SolidPattern)
        painter.setBrush(brush)
        rect2 = QRect(0,0,65,30)
        painter.drawRect(rect2)
        painter.end()



class gameLogic(MainWindowDis):
    def __init__(self):
        MainWindowDis.__init__(self)
        self.gameRun = True
        self.gamePaused = False
        self.xDist = -5
        self.yDist = -5
        self.turnCount = 0
        self.turnsAllowed = 4
        self.winAnnimation()
        self.playGame(self.gameRun)
        

    def ballMove(self, xDist, yDist):
        self.currentBallPosition = self.ball.pos()
        self.newBallMove = QPoint(self.xDist, self.yDist) 
        self.newBallPosition = self.currentBallPosition + self.newBallMove
        self.ball.move(self.newBallPosition)

    def ballBounce(self, xBounce, yBounce):
        if xBounce:
            self.xDist*= -1
            self.ballMove(self.xDist, self.yDist)
        if yBounce:
            self.yDist*= -1
            self.ballMove(self.xDist,self.yDist)

    def paddleCollision(self):
        self.paddleCurrentPos = self.paddle.pos()
        self.currentBallPosition = self.ball.pos()
        if math.dist([self.currentBallPosition.y()],[self.paddleCurrentPos.y()]) ==20: 
            if math.dist([self.currentBallPosition.x()], [self.paddleCurrentPos.x()]) >=0 and math.dist([self.currentBallPosition.x()], [self.paddleCurrentPos.x()]) <=50:
                    if self.xDist > 0:
                        self.ballBounce(xBounce=True,yBounce=True)
                    elif self.xDist<0:
                        self.ballBounce(xBounce=False,yBounce=True)
            elif math.dist([self.currentBallPosition.x()],[self.paddleCurrentPos.x()])<=150 and math.dist([self.currentBallPosition.x()], [self.paddleCurrentPos.x()]) >100:
                if self.xDist > 0:
                    self.ballBounce(xBounce=False,yBounce=True)
                elif self.xDist<0:
                    self.ballBounce(xBounce=True,yBounce=True)
            elif math.dist([self.currentBallPosition.x()], [self.paddleCurrentPos.x()]) >50 and math.dist([self.currentBallPosition.x()], [self.paddleCurrentPos.x()])<=100: 
                self.ballBounce(xBounce=True,yBounce=True)
            
    def wallCollision(self):
        self.currentBallPosition = self.ball.pos()
        if self.currentBallPosition.x()<=0:
            self.ballBounce(xBounce=True,yBounce=False)
        if self.currentBallPosition.x() >= self.windowWidth-20:
            self.ballBounce(xBounce=True,yBounce=False)
        if self.currentBallPosition.y() <= 0:
            self.ballBounce(xBounce=False,yBounce=True)
        if self.currentBallPosition.y() > 560:  
            self.gameRun = False
            self.resetGame()
    
    def brickCollision(self):
        global bricks 
        brickLen = 65
        brickWid = 35
        self.currentBallPosition = self.ball.pos()      
        for i in self.gridList:
            for j in i:
                self.currentBrickPosition = j.pos()
                if math.dist([self.currentBallPosition.x(),self.currentBallPosition.y()], [self.currentBrickPosition.x(),self.currentBrickPosition.y()]) < 70:
                    if self.currentBallPosition.y() == self.currentBrickPosition.y() + brickWid and self.yDist<0:
                        self.ballBounce(xBounce=False,yBounce=True)
                        j.move(5000,5000)
                        i.remove(j)
                        if len(i) == 0:
                            self.gridList.remove(i)
                            self.checkWin()
                    elif self.currentBallPosition.y() - self.currentBrickPosition.y() == -15 and self.yDist > 0:
                        self.ballBounce(xBounce=False,yBounce=True)
                        j.move(5000,5000)
                        i.remove(j)
                        if len(i) == 0:
                            self.gridList.remove(i)
                            self.checkWin()
                        elif self.currentBallPosition.x() == self.currentBrickPosition.x() and self.xDist>0:
                            self.ballBounce(xBounce=True,yBounce=False)
                            j.move(5000,5000)
                            i.remove(j)
                            if len(i) == 0:
                                self.gridList.remove(i)
                                self.checkWin()
                        elif self.currentBallPosition.x() == self.currentBrickPosition.x() + brickLen and self.xDist<0:
                            self.ballBounce(xBounce=True,yBounce=False)
                            j.move(5000,5000)
                            i.remove(j)
                            if len(i) == 0:
                                self.gridList.remove(i)
                                self.checkWin()
                        
    def winAnnimation(self):
        self.winLabel = QLabel()
        self.winLabel.setGeometry(300,300,500,350)
        self.layout.addWidget(self.winLabel)
        self.winGif = QMovie("/home/zain/Downloads/winGif.gif")
        self.winLabel.setMovie(self.winGif)
        self.winGif.setScaledSize(QSize(350,350))
    
    def checkWin(self):
    	if len(self.gridList) == 0:
            self.gameRun = False
            self.winGif.start()
    
    def playGame(self,gameRun):
        while self.gameRun:
            self.update()
            QApplication.processEvents()
            time.sleep(0.01)
            self.ballMove(self.xDist,self.yDist)
            self.paddleCollision()
            self.wallCollision()
            self.brickCollision()
    
    def resetGame(self):
        self.turnCount += 1
        if self.turnCount <= self.turnsAllowed:
            self.gameRun = True
            self.xDist = -5
            self.yDist = -5
            self.uiComponents()
            self.brickGrid()
            self.playGame(self.gameRun)


app = QApplication(sys.argv)
gL = gameLogic()
sys.exit(app.exec())