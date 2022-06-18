import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
from utils.stream import Stream

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        self.stream = Stream()
        self.stream.changeMap.connect(self.onPixmap)
        self.stream.isOpened.connect(self.isOpened)
        self.stream.start()

    def onPixmap(self, pixmap):
        self.frame.setPixmap(pixmap)

    def isOpened(self, flag):
        pass

    def closeEvent(self, event):
        self.stream.terminate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
