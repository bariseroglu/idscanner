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
        self.stream.isValid.connect(self.isValid)
        self.stream.onData.connect(self.onData)
        self.stream.start()

    def onPixmap(self, pixmap):
        self.frame.setPixmap(pixmap)

    def isOpened(self, flag):
        pass

    def isValid(self, result):
        if result.status:
            self.status.setText('Valid Input, ' + result.face + ' Face')
        else:
            self.status.setText('Invalid Input')

    def onData(self, data):
        if data.id != '': self.id.setText('ID: ' + data.id)
        if data.surname != '': self.surname.setText('SURNAME: ' + data.surname)
        if data.name != '': self.name.setText('NAME: ' + data.name)
        if data.date != '': self.date.setText('DATE OF BIRTH: ' + data.date)
        if data.documentNo != '': self.documentNo.setText('DOCUMENT NO: ' + data.documentNo)
        if data.validDate != '': self.date.setText('VALID UNTIL: ' + data.validDate)
        if data.gender != '': self.gender.setText('GENDER: ' + data.gender)

    def closeEvent(self, event):
        self.stream.terminate()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

