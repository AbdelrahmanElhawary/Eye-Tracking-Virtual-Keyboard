# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI\test.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(299, 164)
        self.blank_b = QtWidgets.QPushButton(Form)
        self.blank_b.setGeometry(QtCore.QRect(10, 10, 111, 41))
        self.blank_b.setObjectName("blank_b")
        self.right_blank_b = QtWidgets.QPushButton(Form)
        self.right_blank_b.setGeometry(QtCore.QRect(10, 110, 111, 41))
        self.right_blank_b.setObjectName("right_blank_b")
        self.left_blank_b = QtWidgets.QPushButton(Form)
        self.left_blank_b.setGeometry(QtCore.QRect(130, 60, 161, 51))
        self.left_blank_b.setObjectName("left_blank_b")
        self.right_b = QtWidgets.QPushButton(Form)
        self.right_b.setGeometry(QtCore.QRect(70, 60, 51, 41))
        self.right_b.setObjectName("right_b")
        self.left_b = QtWidgets.QPushButton(Form)
        self.left_b.setGeometry(QtCore.QRect(10, 60, 51, 41))
        self.left_b.setObjectName("left_b")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Test"))
        self.blank_b.setText(_translate("Form", "Blank"))
        self.right_blank_b.setText(_translate("Form", "RightBlank(Down)"))
        self.left_blank_b.setText(_translate("Form", "Left Blank(stop and start)"))
        self.right_b.setText(_translate("Form", "Right"))
        self.left_b.setText(_translate("Form", "Left"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
