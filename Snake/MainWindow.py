from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QPushButton
from MainBoard import Board


class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_board = Board(self)
        self.restart_pause_button = QPushButton('开始', self)
        self.reset_button = QPushButton('重新开始', self)

        self.status_bar = self.statusBar()

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.main_board)
        self.restart_pause_button.move(1000, 100)
        self.reset_button.move(1000, 200)

        self.reset_button.clicked.connect(self.main_board.reset)
        self.restart_pause_button.clicked.connect(self.restart_pause)

        self.main_board.start()

        self.resize(1200, 900)
        self.setMinimumSize(1200, 900)

        self.center()
        self.setWindowTitle('Snake')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    def restart_pause(self, pressed):
        if pressed:
            self.restart_pause_button.setText('暂停')
        else:
            self.restart_pause_button.setText('开始')
