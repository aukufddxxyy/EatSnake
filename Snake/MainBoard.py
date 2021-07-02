from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QKeyEvent, QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QBasicTimer, QTimerEvent
from Snake import Snake


class Board(QFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.is_started = False

        self.size = 41
        self.speed = 100
        self.snake = Snake(self.size)

        self.rate = 0.9

        self.timer = QBasicTimer()
        self.direction = 0

        self.init_board()

    def init_board(self):
        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        self.timer.start(self.speed, self)

    def paintEvent(self, event):
        qp = QPainter(self)
        rect = self.contentsRect()
        self.draw_map(qp, rect.top(), rect.bottom(), rect.left(), rect.right())
    
    def draw_map(self, qp: QPainter, t, b, l, r):
        color = QColor(0x000000)
        width = min([b-t, r-l])

        qp.fillRect(l, t, width, width, color)

        b_w = width*self.rate//self.size
        m_p = (width-b_w*self.size) // 2

        pen = QPen(Qt.white, 1, Qt.SolidLine)
        qp.setPen(pen)
        # 下
        qp.drawLine(m_p, m_p+self.size*b_w, m_p+self.size*b_w, m_p+self.size*b_w)
        # 右
        qp.drawLine(m_p+self.size*b_w, m_p, m_p+self.size*b_w, m_p+self.size*b_w)
        # 左
        qp.drawLine(m_p, m_p, m_p, m_p+self.size*b_w)
        # 上
        qp.drawLine(m_p, m_p, m_p+self.size*b_w, m_p)
        
        self.draw_food(qp, b_w, m_p)
        self.draw_snake(qp, b_w, m_p)
        
    def draw_snake(self, qp: QPainter, b_w, m_p):
        colors = [0x00BFFF, 0x4EEE94]

        for i in self.snake.body:
            y = i[0]
            x = i[1]
            qp.fillRect(x*b_w+m_p+1, y*b_w+m_p+1, b_w-2, b_w-2, QColor(colors[1]))

        qp.fillRect(self.snake.head[1]*b_w+m_p+1, self.snake.head[0]*b_w+m_p+1, b_w-2, b_w-2, QColor(colors[0]))

    def draw_food(self, qp: QPainter, b_w, m_p):
        color = QColor(0xFF7F50)

        qp.fillRect(self.snake.food[1]*b_w+m_p+1, self.snake.food[0]*b_w+m_p+1, b_w-2, b_w-2, color)

    def pause_restart(self):
        self.is_started = not self.is_started
        if self.is_started:
            self.start()
        else:
            self.timer.stop()

    def reset(self):
        if not self.is_started:
            self.timer.stop()
            self.snake = Snake(self.size)
            self.update()

    def timerEvent(self, event: QTimerEvent) -> None:
        if event.timerId() == self.timer.timerId():
            if self.is_started:
                self.snake.change_direction(self.direction)
                self.snake.move()
                self.update()
        else:
            super().timerEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self.pause_restart()
        if self.is_started:
            if event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
                self.direction = 0
            elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
                self.direction = 1
            elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
                self.direction = 2
            elif event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
                self.direction = 3
