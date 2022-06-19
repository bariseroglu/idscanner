from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui
import cv2
from utils.recognize import Recognize

class Stream(QThread):

    changeMap = pyqtSignal('QPixmap')
    isValid = pyqtSignal(object)
    onData = pyqtSignal(object)
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
        recognize = Recognize()
        while True:
            if not self.__run: break
            success, frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
            h, w, ch = frame.shape
            m = (w / 2, h / 2)
            s = w / 3
            y = int(m[1] - s / 1.5)
            x = int(m[0] - s)
            bytesPerLine = ch * w
            color = (255,0,0)
            result = recognize.isValid(self.cropImage(thresh1, x, y, m))
            self.isValid.emit(result)
            if result.status:
                color = (0,255,0)
                data = recognize.recognize(self.cropImage(thresh1, x, y, m))
                self.onData.emit(data)
            cv2.rectangle(frame, (int(m[0] - s), int(m[1] - s/1.5)), (int(m[0] + s), int(m[1] + s/1.5)), color, 2)
            qtFormat = QtGui.QImage(frame.data, w, h, bytesPerLine, QtGui.QImage.Format.Format_RGB888)
            c = qtFormat.scaled(960, 480)
            self.changeMap.emit(QPixmap.fromImage(c))
        cap.release()

    def cropImage(self, frame, x, y, m):
        return frame[y:y + int(m[1] - y) * 2, x:x + int(m[0] - x) * 2]

    def terminate(self):
        self.__run = False
