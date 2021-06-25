from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QKeyEvent, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
import random
from Snake import Snake


class Board(QFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.is_started = False
        self.key_signal = True

        self.map_width = 41
        self.blanks = []
        for i in range(self.map_width):
            for j in range(self.map_width):
                self.blanks.append((i, j))

        self.snake = Snake((self.map_width//2, self.map_width//2), self.map_width)
        for i in self.snake.body:
            self.blanks.remove(i)

        self.food = self.new_food()

        self.margin = 20
        self.padding = 50
        self.m_p = self.margin+self.padding

        self.timer = QBasicTimer()

        self.init_board()

    def init_board(self):
        self.setFocusPolicy(Qt.StrongFocus)
    
    def new_food(self):
        return random.choice(self.blanks)

    def change_blanks(self, t: tuple):
        if len(t) == 2:
            for i in t[0]:
                self.blanks.append(i)
            self.blanks.remove(t[1])

    def square_size(self):
        square_width = (self.contentsRect().width()-self.m_p*2) // self.map_width
        return square_width

    def start(self):
        self.timer.start(100, self)

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = self.contentsRect()
        self.draw_map(qp, rect.top(), rect.bottom(), rect.left(), rect.right())
    
    def draw_map(self, qp: QPainter, t, b, l, r):
        color = QColor(0xDEB887)
        width = min([b-t, r-l])

        qp.fillRect(l, t, width, width, color)

        pen = QPen(Qt.black, 4, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.margin,self.margin,width-self.margin,self.margin)
        qp.drawLine(self.margin,self.margin,self.margin,width-self.margin)
        qp.drawLine(width-self.margin,self.margin,width-self.margin,width-self.margin)
        qp.drawLine(self.margin,width-self.margin,width-self.margin,width-self.margin)

        board_width = (width-2*self.m_p)//self.map_width
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.m_p, self.m_p+self.map_width*board_width, self.m_p+self.map_width*board_width, self.m_p+self.map_width*board_width)
        qp.drawLine(self.m_p+self.map_width*board_width, self.m_p, self.m_p+self.map_width*board_width, self.m_p+self.map_width*board_width)
        qp.drawLine(self.m_p, self.m_p, self.m_p, self.m_p+self.map_width*board_width)
        qp.drawLine(self.m_p, self.m_p, self.m_p+self.map_width*board_width, self.m_p)
        
        self.draw_food(qp, board_width)
        self.draw_snake(qp, board_width)
        
    def draw_snake(self,qp: QPainter, b_w):
        color = QColor(0x4EEE94)

        for i in self.snake.body:
            y = i[0]
            x = i[1]
            qp.fillRect(x*b_w+self.m_p+1, y*b_w+self.m_p+1, b_w-2, b_w-2, color)

    def draw_food(self, qp: QPainter, b_w):
        color = QColor(0xFF7F50)

        qp.fillRect(self.food[1]*b_w+self.m_p+1, self.food[0]*b_w+self.m_p+1, b_w-2, b_w-2, color)

    def pause_restart(self):
        self.is_started = not self.is_started
        if self.is_started:
            self.start()
        else:
            self.timer.stop()

    def reset(self):
        pass

    def timerEvent(self, event: QTimerEvent) -> None:
        if event.timerId() == self.timer.timerId():
            if self.is_started:
                self.key_signal = not self.key_signal
                temp = self.snake.move(self.food)
                self.change_blanks(temp[1])
                if temp[0]:
                    self.food = self.new_food()
                self.key_signal = not self.key_signal
                self.update()
        else:
            super().timerEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if self.key_signal:
            if event.key() == Qt.Key_Space:
                self.key_signal =True
                self.pause_restart()
            if self.is_started:
                if event.key() == Qt.Key_Up:
                    self.snake.change_direction(0)
                elif event.key() == Qt.Key_Down:
                    self.snake.change_direction(1)
                elif event.key() == Qt.Key_Right:
                    self.snake.change_direction(2)
                elif event.key() == Qt.Key_Left:
                    self.snake.change_direction(3)
        