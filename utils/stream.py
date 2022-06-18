from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui
import cv2
class Stream(QThread):

    changeMap = pyqtSignal('QPixmap')
    isOpened = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.__run = True

    def run(self):
        cap = cv2.VideoCapture(0)
        if cap is None or not cap.isOpened():
            self.isOpened.emit(False)
        else:
            self.isOpened.emit(True)
        while True:
            if not self.__run: break
            success, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            qtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format.Format_RGB888)
            c = qtFormat.scaled(960, 480, Qt.AspectRatioMode.KeepAspectRatio)
            self.changeMap.emit(QPixmap.fromImage(c))
        cap.release()

    def terminate(self):
        self.__run = False