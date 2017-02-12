from PyQt4 import QtCore, QtGui

class KeyButton(QtGui.QPushButton):

    def __init__(self, parent=None):
        QtGui.QPushButton.__init__(self, parent)

    def setKeyboard(self, keyboard):
        self.keyboard = keyboard

    def setString(self, string):
        self.string = string

    def setup(self, keyboard, string):
        self.setKeyboard(keyboard)
        self.setString(string)

    def mousePressEvent(self, event):
        self.keyboard.press(self.string)

    def mouseReleaseEvent(self, event):
        self.keyboard.unpress(self.string)


