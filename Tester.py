from GUI import testk
from PyQt5.QtWidgets import QWidget
from Controller import Controller
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import sys
class TestVK(QWidget, testk.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setGeometry(0, 0, 400, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowDoesNotAcceptFocus)
        self.vk = Controller()
        self.vk.show()
        self.vk.setFocus()
        self.blank_b.clicked.connect(self.blankClicked)
        self.right_blank_b.clicked.connect(self.rightBlanckstopClicked)
        self.left_blank_b.clicked.connect(self.leftBlanckClicked)
        self.right_b.clicked.connect(self.rightClicked)
        self.left_b.clicked.connect(self.leftClicked)
        self.left_blank_b.setShortcut('up')
        self.right_blank_b.setShortcut('down')
        self.right_b.setShortcut('right')
        self.left_b.setShortcut('left')
        self.blank_b.setShortcut('space')
    def blankClicked(self):
        if self.vk.mouse_state:
            self.vk.mouseController('blank')
        else :
            self.vk.setFocus()
            self.vk.vkController('blank')

    def rightBlanckstopClicked(self):
        if self.vk.mouse_state:
            self.vk.mouseController('blank')
        else :
            self.vk.vkController('right_blank')

    def leftBlanckClicked(self):
        if self.vk.mouse_state:
            self.vk.mouseController('blank')
        else :
            self.vk.vkController('left_blank')

    def rightClicked(self):
        if self.vk.mouse_state:
            self.vk.mouseController('blank')
        else :
            self.vk.vkController('right')

    def leftClicked(self):
        if self.vk.mouse_state:
            self.vk.mouseController('blank')
        else :
            self.vk.vkController('left')

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = TestVK()
    win.show()
    sys.exit(app.exec_())