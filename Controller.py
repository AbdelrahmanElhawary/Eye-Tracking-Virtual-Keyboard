import csv, keyboard, qdarkstyle,pyttsx3
from Threads import MouseThread,CurserThread,EyeTrackerThread,Prediction
from GUI import VKDesign
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt,QThread
from pynput.mouse import Button

class Controller(QMainWindow, VKDesign.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Attributes
        self.button_to_key_dic = {}
            #here we link objectName to Key Command Filled from MapKeys.csv
        self.button_to_stylesheet_dic = {}
            #here we link obkectName to Main style sheet for each button
        self.two_d_buttons = list()
            #here we divide button to rows and columns to move in it by Curser thread
        self.curser_thread = CurserThread(self.two_d_buttons)
            #here we make object form Curser thread to use this obkect in Controller
        self.eye_tracker_thread = EyeTrackerThread()
            # here we make object form EyeTracker thread to use this obkect in Controller
        self.mouse_thread=MouseThread()
            # here we make object form Mouse thread to use this obkect in Controller
        self.word_prediction=Prediction()
            # here we make object form WordPrediction thread to use this obkect in Controller
        self.chosen_key = None
            #make reference for chosen key in curser thread
        self.prev_key = None
            #make reference for prev key in curser thread
        self.caps_bool = False
            #To Know if caps_look button on or of
        self.shift_bool = False
            #To Know if shift button on or of
        self.ctrl_bool = False
            #To Know if ctrl button on or of
        self.alt_bool = False
            #To Know if alt button on or of
        self.mouse_bool=False
            #To Know if mouse button on or of
        self.curser_state=True
            #To Know the curser state moving or stoped
        self.mouse_state=False
            #To Know the mouse state moving or stoped
        self.speaker = pyttsx3.init()
            #Make opject for TextToSpeech

        # Methods
        self.initUi()
            #here we apply the ui made from QDesigner and Qdarkstyle
        self.connectKeys()
            #here we connect each button in VK MainWindow to Keyboard Conmmad
        self.startCurserThread()
            #here we start the Curser thread
        self.makeButtons2D()
            #here we fill two_d_button list from MapKeys.csv
        self.startEyeTrackerThread()
            #here we start the EyeTracker thread
        self.textEdit.textChanged.connect(self.changeWord)
            #here to get every change in textEdit and send it to Word predection thread
        self.startWordPredection()
            #here we start the wordPredection thread


    def initUi(self):  # modify the UI here
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setupUi(self)
        self.setFixedWidth(802)
        self.setFixedHeight(388)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

    def connectKeys(self):  # connect each button to event
        with open('Resources/CSV/MapKeys.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                self.button_to_key_dic[row[0]] = row[1]
                a = getattr(self, row[0])
                self.button_to_stylesheet_dic[row[0]] = a.styleSheet()
                a.clicked.connect(self.buttonClicked)

    def makeButtons2D(self):
        with open('Resources/CSV/TwoDButtons.csv') as file:
            reader = csv.reader(file)
            for row in reader:
                temp = list()
                for i in row:
                    if i != "":
                        temp.append(i)
                self.two_d_buttons.append(temp)

    def buttonClicked(self):  # all buttons events
        sender = self.sender()
        self.textEdit.setFocus()

        if sender.objectName()=='word_suggest_b1':
            str=''
            if len(self.textEdit.toPlainText()) and self.textEdit.toPlainText()[-1]!=' ':
                str=self.textEdit.toPlainText()
                while len(str) and str[-1]!=' ':
                    str=str[:-1]
                self.textEdit.setText('')
                keyboard.write(str)
        c_key = self.button_to_key_dic[sender.objectName()]
        if c_key in ['shift', 'ctrl', 'alt']:
            self.buttonAction(c_key)
        elif self.button_to_key_dic[sender.objectName()]=='suggest':
            keyboard.write(sender.text()+' ')
        elif sender.objectName()=='text_to_speech_b':
            self.textToSpeech()
        elif sender.objectName()=='mouse_b':
            self.startMouseThread()
        else:
            keyboard.press_and_release(self.button_to_key_dic[sender.objectName()])
            self.boolTrueKey(sender)
        if sender.objectName() == 'caps_lock_b':
            self.caps_bool = not self.caps_bool
            if self.caps_bool:
                sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
            else:
                sender.setStyleSheet(self.button_to_stylesheet_dic[sender.objectName()])
        if self.chosen_key == sender:
            self.chosen_key.setStyleSheet(
                self.button_to_stylesheet_dic[self.chosen_key.objectName()] + "background-color : #1464A0")

    def boolTrueKey(self,sender):
        #   Shift Button
        if self.shift_bool and (sender.objectName() not in ['up_b','right_b','down_b','left_b']):
            self.shift_bool = False
            keyboard.release('shift')
            self.l_shift_b.setStyleSheet(self.button_to_stylesheet_dic['l_shift_b'])
            self.r_shift_b.setStyleSheet(self.button_to_stylesheet_dic['r_shift_b'])
        #  Ctrl Button
        if self.ctrl_bool:
            self.ctrl_bool = False
            keyboard.release('ctrl')
            self.l_ctrl.setStyleSheet(self.button_to_stylesheet_dic['l_ctrl'])
            self.r_ctrl.setStyleSheet(self.button_to_stylesheet_dic['r_ctrl'])
        #  Alt Button
        if self.alt_bool:
            self.alt_bool = False
            keyboard.release('alt')
            self.l_alt_b.setStyleSheet(self.button_to_stylesheet_dic['l_alt_b'])
            self.r_alt_b.setStyleSheet(self.button_to_stylesheet_dic['r_alt_b'])

    def buttonAction(self, key):
        if key == 'shift':
            self.shift_bool = not self.shift_bool
            if self.shift_bool:
                keyboard.press('shift')
                self.l_shift_b.setStyleSheet(self.l_shift_b.styleSheet() + "background-color : #A364A0")
                self.r_shift_b.setStyleSheet(self.r_shift_b.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('shift')
                self.l_shift_b.setStyleSheet(self.button_to_stylesheet_dic['l_shift_b'])
                self.r_shift_b.setStyleSheet(self.button_to_stylesheet_dic['r_shift_b'])
        if key == 'ctrl':
            self.ctrl_bool = not self.ctrl_bool
            if self.ctrl_bool:
                keyboard.press('ctrl')
                self.l_ctrl.setStyleSheet(self.l_ctrl.styleSheet() + "background-color : #A364A0")
                self.r_ctrl.setStyleSheet(self.r_ctrl.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('ctrl')
                self.l_ctrl.setStyleSheet(self.button_to_stylesheet_dic['l_ctrl'])
                self.r_ctrl.setStyleSheet(self.button_to_stylesheet_dic['r_ctrl'])
        if key == 'alt':
            self.alt_bool = not self.alt_bool
            if self.alt_bool:
                keyboard.press('alt')
                self.l_alt_b.setStyleSheet(self.l_alt_b.styleSheet() + "background-color : #A364A0")
                self.r_alt_b.setStyleSheet(self.r_alt_b.styleSheet() + "background-color : #A364A0")
            else:
                keyboard.release('alt')
                self.l_alt_b.setStyleSheet(self.button_to_stylesheet_dic['l_alt_b'])
                self.r_alt_b.setStyleSheet(self.button_to_stylesheet_dic['r_alt_b'])
        if key == 'mouse_b':
            self.mouse_bool = not self.mouse_bool
            if self.mouse_bool:
                self.mouse_b.setStyleSheet(self.mouse_b.styleSheet() + "background-color : #A364A0")
            else:
                self.mouse_b.setStyleSheet(self.button_to_stylesheet_dic['mouse_b'])

    def startCurserThread(self):
        self.curser_thread.change_value.connect(self.controlCurserThread)
        self.curser_thread.start()

    def controlCurserThread(self, val):
        self.chosen_key = getattr(self, val[1])
        self.prev_key = getattr(self, val[0])
        self.prev_key.setStyleSheet(self.button_to_stylesheet_dic[self.prev_key.objectName()])
        self.fixStyleOfLastChosenKey(self.prev_key)
        self.chosen_key.setStyleSheet(
            self.button_to_stylesheet_dic[self.chosen_key.objectName()] + "background-color : #1464A0")

    def vkController(self, comand):
        if self.curser_state:
            if comand=='right_blank':               #Go down
                self.curser_thread.terminate()
                self.chosen_key.setStyleSheet(self.button_to_stylesheet_dic[self.chosen_key.objectName()])
                self.fixStyleOfLastChosenKey(self.chosen_key)
                self.curser_thread.row += 1
                self.curser_thread.row %= 7
                self.curser_thread.column = len(
                    self.two_d_buttons[self.curser_thread.row]) - 1 if self.curser_thread.column >= len(
                    self.two_d_buttons[self.curser_thread.row]) else self.curser_thread.column
                self.curser_thread.start()
            elif comand=='left_blank':  #Stop Curser
                self.curser_state=False
                self.curser_thread.terminate()
            elif comand=='blank':   #press ChosenKey
                # self.chosen_key.click()
                pass
            elif comand=='right':
                pass
            elif comand=='left':pass
            # else :print(f'in vkController this comand unvalid {comand} and state is True')
        else:
            if comand=='right_blank':   #GO Down Step
                self.prev_key = self.chosen_key
                self.prev_key.setStyleSheet(self.button_to_stylesheet_dic[self.prev_key.objectName()])
                self.fixStyleOfLastChosenKey(self.prev_key)
                self.curser_thread.row += 1
                self.curser_thread.row = self.curser_thread.row % 7

                self.curser_thread.column = len(
                    self.two_d_buttons[self.curser_thread.row]) - 1 if self.curser_thread.column >= len(
                    self.two_d_buttons[self.curser_thread.row]) else self.curser_thread.column
                self.chosen_key = getattr(self, self.two_d_buttons[self.curser_thread.row][self.curser_thread.column])
                self.chosen_key.setStyleSheet(
                    self.button_to_stylesheet_dic[self.chosen_key.objectName()] + "background-color : #1464A0")
            elif comand=='left_blank': #continue
                self.curser_state=True
                self.curser_thread.start()
            elif comand=='blank':self.chosen_key.click()
            elif comand=='right':   #Go right Step
                self.prev_key = self.chosen_key
                self.prev_key.setStyleSheet(self.button_to_stylesheet_dic[self.prev_key.objectName()])
                self.fixStyleOfLastChosenKey(self.prev_key)
                self.curser_thread.column += 1
                self.curser_thread.column = self.curser_thread.column % len(self.two_d_buttons[self.curser_thread.row])
                self.chosen_key = getattr(self, self.two_d_buttons[self.curser_thread.row][self.curser_thread.column])
                self.chosen_key.setStyleSheet(
                    self.button_to_stylesheet_dic[self.chosen_key.objectName()] + "background-color : #1464A0")
            elif comand=='left':    # Go Left Step
                self.prev_key = self.chosen_key
                self.prev_key.setStyleSheet(self.button_to_stylesheet_dic[self.prev_key.objectName()])
                self.fixStyleOfLastChosenKey(self.prev_key)
                self.curser_thread.column -= 1
                self.curser_thread.column = (self.curser_thread.column + len(
                    self.two_d_buttons[self.curser_thread.row])) % len(
                    self.two_d_buttons[self.curser_thread.row])
                self.chosen_key = getattr(self, self.two_d_buttons[self.curser_thread.row][self.curser_thread.column])
                self.chosen_key.setStyleSheet(
                    self.button_to_stylesheet_dic[self.chosen_key.objectName()] + "background-color : #1464A0")
            # else :print(f'in vkController this comand unvalid {comand} and state is False')

    def fixStyleOfLastChosenKey(self, sender):
        if self.button_to_key_dic[sender.objectName()] == 'caps_lock' and self.caps_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()] == 'shift' and self.shift_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()] == 'ctrl' and self.ctrl_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")
        if self.button_to_key_dic[sender.objectName()] == 'alt' and self.alt_bool:
            sender.setStyleSheet(sender.styleSheet() + "background-color : #A364A0")

    def startEyeTrackerThread(self):
        self.eye_tracker_thread.change_value.connect(self.controlEyeTrackerThread)
        self.eye_tracker_thread.start(QThread.HighPriority)

    def controlEyeTrackerThread(self, val):
        if self.mouse_bool:
            self.mouseController(val)
        else:
            self.vkController(val)

    def textToSpeech(self):
        selected_text=self.textEdit.textCursor().selection().toPlainText()
        self.speaker.say(selected_text if len(selected_text)>0 else self.textEdit.toPlainText())
        self.speaker.runAndWait()

    def startMouseThread(self):
        self.buttonAction('mouse_b')
        if self.curser_state:
            self.curser_state = False
            self.curser_thread.terminate()
            self.mouse_state = True
            self.mouse_thread.change_value.connect(self.controlMouseThread)
            self.mouse_thread.start()
        else:
            self.curser_state = True
            self.curser_thread.start()
            self.mouse_state=False
            self.mouse_thread.terminate()
            return

    def controlMouseThread(self,val):
        pass

    def mouseController(self,val):
        if self.mouse_state:
            if val=='blank':
                self.mouse_state=False
                self.mouse_thread.terminate()
            elif val=='right':
                self.mouse_thread.terminate()
                self.mouse_thread.moving_x=5
                self.mouse_thread.moving_y=0
                self.mouse_thread.start()
            elif val=='left':
                self.mouse_thread.terminate()
                self.mouse_thread.moving_x = -5
                self.mouse_thread.moving_y = 0
                self.mouse_thread.start()
            elif val=='right_blank':
                self.mouse_thread.terminate()
                self.mouse_thread.moving_x = 0
                self.mouse_thread.moving_y = 5
                self.mouse_thread.start()
            elif val=='left_blank':
                self.mouse_thread.terminate()
                self.mouse_thread.moving_x = 0
                self.mouse_thread.moving_y = -5
                self.mouse_thread.start()
        else:
            if val=='blank':
                self.mouse_thread.controller.click(Button.left, 2)
            elif val in ['right','left']:
                self.mouse_state=True
                self.mouse_thread.start()
            elif val=='right_blank':
                self.mouse_thread.controller.click(Button.right, 1)
            elif val=='left_blank':
                self.mouse_thread.controller.click(Button.left, 1)

    def startWordPredection(self):
        self.word_prediction.change_value.connect(self.controlWordPredection)
        self.word_prediction.start()

    def controlWordPredection(self,val):
        self.word_suggest_b1.setText(val[0])
        self.word_suggest_b2.setText(val[1])
        self.word_suggest_b3.setText(val[2])
        self.word_suggest_b4.setText(val[3])
        self.word_suggest_b5.setText(val[4])

    def changeWord(self):
        self.word_prediction.Words=self.textEdit.toPlainText()