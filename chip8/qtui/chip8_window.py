# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chip8_window.ui'
#
# Created by: PyQt4 UI code generator 4.12
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(380, 334)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout.addWidget(self.graphicsView)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.one_button = QtGui.QPushButton(self.centralwidget)
        self.one_button.setObjectName(_fromUtf8("one_button"))
        self.gridLayout.addWidget(self.one_button, 0, 0, 1, 1)
        self.two_button = QtGui.QPushButton(self.centralwidget)
        self.two_button.setObjectName(_fromUtf8("two_button"))
        self.gridLayout.addWidget(self.two_button, 0, 1, 1, 1)
        self.three_button = QtGui.QPushButton(self.centralwidget)
        self.three_button.setObjectName(_fromUtf8("three_button"))
        self.gridLayout.addWidget(self.three_button, 0, 2, 1, 1)
        self.c_button = QtGui.QPushButton(self.centralwidget)
        self.c_button.setObjectName(_fromUtf8("c_button"))
        self.gridLayout.addWidget(self.c_button, 0, 3, 1, 1)
        self.four_button = QtGui.QPushButton(self.centralwidget)
        self.four_button.setObjectName(_fromUtf8("four_button"))
        self.gridLayout.addWidget(self.four_button, 1, 0, 1, 1)
        self.five_button = QtGui.QPushButton(self.centralwidget)
        self.five_button.setObjectName(_fromUtf8("five_button"))
        self.gridLayout.addWidget(self.five_button, 1, 1, 1, 1)
        self.six_button = QtGui.QPushButton(self.centralwidget)
        self.six_button.setObjectName(_fromUtf8("six_button"))
        self.gridLayout.addWidget(self.six_button, 1, 2, 1, 1)
        self.d_button = QtGui.QPushButton(self.centralwidget)
        self.d_button.setObjectName(_fromUtf8("d_button"))
        self.gridLayout.addWidget(self.d_button, 1, 3, 1, 1)
        self.seven_button = QtGui.QPushButton(self.centralwidget)
        self.seven_button.setObjectName(_fromUtf8("seven_button"))
        self.gridLayout.addWidget(self.seven_button, 2, 0, 1, 1)
        self.eight_button = QtGui.QPushButton(self.centralwidget)
        self.eight_button.setObjectName(_fromUtf8("eight_button"))
        self.gridLayout.addWidget(self.eight_button, 2, 1, 1, 1)
        self.nine_button = QtGui.QPushButton(self.centralwidget)
        self.nine_button.setObjectName(_fromUtf8("nine_button"))
        self.gridLayout.addWidget(self.nine_button, 2, 2, 1, 1)
        self.e_button = QtGui.QPushButton(self.centralwidget)
        self.e_button.setObjectName(_fromUtf8("e_button"))
        self.gridLayout.addWidget(self.e_button, 2, 3, 1, 1)
        self.a_button = QtGui.QPushButton(self.centralwidget)
        self.a_button.setObjectName(_fromUtf8("a_button"))
        self.gridLayout.addWidget(self.a_button, 3, 0, 1, 1)
        self.zero_button = QtGui.QPushButton(self.centralwidget)
        self.zero_button.setObjectName(_fromUtf8("zero_button"))
        self.gridLayout.addWidget(self.zero_button, 3, 1, 1, 1)
        self.b_button = QtGui.QPushButton(self.centralwidget)
        self.b_button.setObjectName(_fromUtf8("b_button"))
        self.gridLayout.addWidget(self.b_button, 3, 2, 1, 1)
        self.f_button = QtGui.QPushButton(self.centralwidget)
        self.f_button.setObjectName(_fromUtf8("f_button"))
        self.gridLayout.addWidget(self.f_button, 3, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "chip8", None))
        self.one_button.setText(_translate("MainWindow", "1", None))
        self.two_button.setText(_translate("MainWindow", "2", None))
        self.three_button.setText(_translate("MainWindow", "3", None))
        self.c_button.setText(_translate("MainWindow", "C", None))
        self.four_button.setText(_translate("MainWindow", "4", None))
        self.five_button.setText(_translate("MainWindow", "5", None))
        self.six_button.setText(_translate("MainWindow", "6", None))
        self.d_button.setText(_translate("MainWindow", "D", None))
        self.seven_button.setText(_translate("MainWindow", "7", None))
        self.eight_button.setText(_translate("MainWindow", "8", None))
        self.nine_button.setText(_translate("MainWindow", "9", None))
        self.e_button.setText(_translate("MainWindow", "E", None))
        self.a_button.setText(_translate("MainWindow", "A", None))
        self.zero_button.setText(_translate("MainWindow", "0", None))
        self.b_button.setText(_translate("MainWindow", "B", None))
        self.f_button.setText(_translate("MainWindow", "F", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
