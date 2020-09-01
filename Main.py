from Controller import Controller
from PyQt5.QtWidgets import QApplication
import sys
import WordPrediction



if __name__=='__main__':
    WordPrediction.fillModel()
    app = QApplication(sys.argv)
    win = Controller()
    win.show()
    sys.exit(app.exec_())