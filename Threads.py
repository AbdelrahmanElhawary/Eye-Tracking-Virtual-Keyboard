from PyQt5.QtCore import QThread,pyqtSignal
from win32api import GetSystemMetrics
from pynput.mouse import Controller
from EyeTrackerV2 import Detection
import time
from WordPrediction import predict_word


class EyeTrackerThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.d=Detection()


    change_value = pyqtSignal(str)

    def run(self):
        pre = 'open'
        while True:
            cur = self.d.maxIn10Frames()
            if cur != pre and cur == 'open':
                self.change_value.emit(pre)
                print(pre)
            pre = cur

class CurserThread(QThread):

    def __init__(self, two_d_buttons):
        QThread.__init__(self)
        self.twoDButtons = two_d_buttons
        self.row = 0
        self.column = 0

    change_value = pyqtSignal(tuple)    #this signal has chosen key and prev key

    def run(self):
        while True:
            time.sleep(.8)
            prev_key = self.twoDButtons[self.row][self.column]
            self.column += 1
            self.column = self.column % len(self.twoDButtons[self.row])
            self.change_value.emit((prev_key, self.twoDButtons[self.row][self.column]))

class MouseThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.controller = Controller()
        self.moving_x = 0
        self.moving_y = 25
        self.mxHeight=GetSystemMetrics(1)
        self.mxWidth=GetSystemMetrics(0)

    change_value = pyqtSignal(str)

    def run(self):
        while True:
            time.sleep(.2)
            self.controller.move(self.moving_x,self.moving_y)
            pos=self.controller.position

            if self.moving_y:
                if self.moving_y>0:
                    if pos[1]>=self.mxHeight-1:
                        self.moving_y=-self.moving_y
                else:
                    if pos[1]<=0:
                        self.moving_y=-self.moving_y
            else :
                if self.moving_x > 0:
                    if pos[0] >= self.mxWidth-1:
                        self.moving_x = -self.moving_x
                else:
                    if pos[0] <= 0:
                        self.moving_x = -self.moving_x

            self.change_value.emit("")

class Prediction(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.Words=""
        self.Bool=False

    change_value = pyqtSignal(list)
    def fillBool(self):
        ch=' '
        if len(self.Words):
            ch=self.Words[-1]
        else: return False

        if ch.isalpha():
            return True
        else: return False
    def run(self):
        while True:
            time.sleep(.5)
            self.Bool=self.fillBool()
            try:
                lst=predict_word(self.Words,self.Bool)
            except Exception as ex:
                lst=['','','','','']
                print(ex)
            self.change_value.emit(list(lst))

