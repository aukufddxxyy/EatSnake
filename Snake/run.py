import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import SnakeGame

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = SnakeGame()
    sys.exit(app.exec_())
