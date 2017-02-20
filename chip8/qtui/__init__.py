import sys
import os.path
sys.path.append(os.path.abspath(    # Make sure we can import Chip8.
    os.path.join(os.path.dirname(__file__), os.path.pardir)))

from PyQt4 import QtCore, QtGui

from . import chip8_window
import chip8


class Chip8Window(QtGui.QMainWindow,
        chip8_window.Ui_MainWindow):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        fn = QtGui.QFileDialog.getOpenFileName()
        if not fn:
            sys.exit(0)
        self.vm = chip8.Chip8(fn)
        self.vm_thread = VMThread(self.vm)
        self.vm_thread.start()

        self.qsize = QtCore.QSize(
            self.vm.display.WIDTH, self.vm.display.HEIGHT)
        bmp = QtGui.QBitmap(self.qsize)
        bmp.fill(QtCore.Qt.color1)

        self.scene = QtGui.QGraphicsScene(self.graphicsView)
        self.bmp_item = self.scene.addPixmap(bmp)
        self.graphicsView.setScene(self.scene)

        FPS = 30
        screen_timer = QtCore.QTimer(self)
        screen_timer.timeout.connect(self.updateScreen)
        screen_timer.start((1 / FPS) * 1000)
        self.old_pdata = None

        keyboard = self.vm.keyboard
        self.one_button.setup(keyboard, "1")
        self.two_button.setup(keyboard, "2")
        self.three_button.setup(keyboard, "3")
        self.four_button.setup(keyboard, "4")
        self.five_button.setup(keyboard, "5")
        self.six_button.setup(keyboard, "6")
        self.seven_button.setup(keyboard, "7")
        self.eight_button.setup(keyboard, "8")
        self.nine_button.setup(keyboard, "9")
        self.zero_button.setup(keyboard, "0")
        self.a_button.setup(keyboard, "A")
        self.b_button.setup(keyboard, "B")
        self.c_button.setup(keyboard, "C")
        self.d_button.setup(keyboard, "D")
        self.e_button.setup(keyboard, "E")
        self.f_button.setup(keyboard, "F")

    def updateScreen(self):
        pixeldata = self.vm.display.get_data()
        if pixeldata != self.old_pdata:
            new_bmp = QtGui.QBitmap.fromData(
                self.qsize, pixeldata, format=QtGui.QImage.Format_Mono)
            self.bmp_item.setPixmap(new_bmp)
            self.old_pdata = pixeldata

    def showEvent(self, event):
        self.graphicsView.fitInView(
            self.scene.sceneRect(), mode=QtCore.Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.graphicsView.fitInView(
            self.scene.sceneRect(), mode=QtCore.Qt.KeepAspectRatio)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            event.ignore()
            return
        self.grabKeyboard()
        key = event.key()
        keyboard = self.vm.keyboard

        if key == QtCore.Qt.Key_1:
            keyboard.press("1")
            self.one_button.setFlat(True)
        elif key == QtCore.Qt.Key_2:
            keyboard.press("2")
            self.two_button.setFlat(True)
        elif key == QtCore.Qt.Key_3:
            keyboard.press("3")
            self.three_button.setFlat(True)
        elif key == QtCore.Qt.Key_4:
            keyboard.press("4")
            self.four_button.setFlat(True)
        elif key == QtCore.Qt.Key_5:
            keyboard.press("5")
            self.five_button.setFlat(True)
        elif key == QtCore.Qt.Key_6:
            keyboard.press("6")
            self.six_button.setFlat(True)
        elif key == QtCore.Qt.Key_7:
            keyboard.press("7")
            self.seven_button.setFlat(True)
        elif key == QtCore.Qt.Key_8:
            keyboard.press("8")
            self.eight_button.setFlat(True)
        elif key == QtCore.Qt.Key_9:
            keyboard.press("9")
            self.nine_button.setFlat(True)
        elif key == QtCore.Qt.Key_0:
            keyboard.press("0")
            self.zero_button.setFlat(True)
        elif key == QtCore.Qt.Key_A:
            keyboard.press("A")
            self.a_button.setFlat(True)
        elif key == QtCore.Qt.Key_B:
            keyboard.press("B")
            self.b_button.setFlat(True)
        elif key == QtCore.Qt.Key_C:
            keyboard.press("C")
            self.c_button.setFlat(True)
        elif key == QtCore.Qt.Key_D:
            keyboard.press("D")
            self.d_button.setFlat(True)
        elif key == QtCore.Qt.Key_E:
            keyboard.press("E")
            self.e_button.setFlat(True)
        elif key == QtCore.Qt.Key_F:
            keyboard.press("F")
            self.f_button.setFlat(True)

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            event.ignore()
            return
        key = event.key()
        keyboard = self.vm.keyboard

        if key == QtCore.Qt.Key_1:
            keyboard.unpress("1")
            self.one_button.setFlat(False)
        elif key == QtCore.Qt.Key_2:
            keyboard.unpress("2")
            self.two_button.setFlat(False)
        elif key == QtCore.Qt.Key_3:
            keyboard.unpress("3")
            self.three_button.setFlat(False)
        elif key == QtCore.Qt.Key_4:
            keyboard.unpress("4")
            self.four_button.setFlat(False)
        elif key == QtCore.Qt.Key_5:
            keyboard.unpress("5")
            self.five_button.setFlat(False)
        elif key == QtCore.Qt.Key_6:
            keyboard.unpress("6")
            self.six_button.setFlat(False)
        elif key == QtCore.Qt.Key_7:
            keyboard.unpress("7")
            self.seven_button.setFlat(False)
        elif key == QtCore.Qt.Key_8:
            keyboard.unpress("8")
            self.eight_button.setFlat(False)
        elif key == QtCore.Qt.Key_9:
            keyboard.unpress("9")
            self.nine_button.setFlat(False)
        elif key == QtCore.Qt.Key_0:
            keyboard.unpress("0")
            self.zero_button.setFlat(False)
        elif key == QtCore.Qt.Key_A:
            keyboard.unpress("A")
            self.a_button.setFlat(False)
        elif key == QtCore.Qt.Key_B:
            keyboard.unpress("B")
            self.b_button.setFlat(False)
        elif key == QtCore.Qt.Key_C:
            keyboard.unpress("C")
            self.c_button.setFlat(False)
        elif key == QtCore.Qt.Key_D:
            keyboard.unpress("D")
            self.d_button.setFlat(False)
        elif key == QtCore.Qt.Key_E:
            keyboard.unpress("E")
            self.e_button.setFlat(False)
        elif key == QtCore.Qt.Key_F:
            keyboard.unpress("F")
            self.f_button.setFlat(False)
        self.releaseKeyboard()


class VMThread(QtCore.QThread):
    
    def __init__(self, vm):
        QtCore.QThread.__init__(self)
        self.vm = vm

    def run(self):
        self.vm.run()


def run():
    app = QtGui.QApplication(sys.argv)
    myapp = Chip8Window()
    myapp.show()
    sys.exit(app.exec_())


