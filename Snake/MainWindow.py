from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QPushButton
from MainBoard import Board


class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_board = Board(self)
        self.reset_button = QPushButton('重新开始', self)

        self.status_bar = self.statusBar()

        self.init_ui()

    def init_ui(self):
        self.setCentralWidget(self.main_board)
        self.reset_button.move(0, 0)

        self.reset_button.clicked.connect(self.main_board.reset)

        self.main_board.start()

        self.resize(500, 500)
        self.setMinimumSize(500, 500)

        self.center()
        self.setWindowTitle('Snake')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
