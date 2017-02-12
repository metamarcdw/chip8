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
        self.screen_timer = QtCore.QTimer(self)
        self.screen_timer.timeout.connect(self.updateScreen)
        self.screen_timer.start((1 / FPS) * 1000)
        self.old_pdata = None

    def updateScreen(self):
        pixeldata = self.vm.display.get_data()
        if pixeldata == self.old_pdata:
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
        if key == QtCore.Qt.Key_1:
            self.vm.keyboard.press("1")
        elif key == QtCore.Qt.Key_2:
            self.vm.keyboard.press("2")
        elif key == QtCore.Qt.Key_3:
            self.vm.keyboard.press("3")
        elif key == QtCore.Qt.Key_4:
            self.vm.keyboard.press("4")
        elif key == QtCore.Qt.Key_5:
            self.vm.keyboard.press("5")
        elif key == QtCore.Qt.Key_6:
            self.vm.keyboard.press("6")
        elif key == QtCore.Qt.Key_7:
            self.vm.keyboard.press("7")
        elif key == QtCore.Qt.Key_8:
            self.vm.keyboard.press("8")
        elif key == QtCore.Qt.Key_9:
            self.vm.keyboard.press("9")
        elif key == QtCore.Qt.Key_0:
            self.vm.keyboard.press("0")
        elif key == QtCore.Qt.Key_A:
            self.vm.keyboard.press("A")
        elif key == QtCore.Qt.Key_B:
            self.vm.keyboard.press("B")
        elif key == QtCore.Qt.Key_C:
            self.vm.keyboard.press("C")
        elif key == QtCore.Qt.Key_D:
            self.vm.keyboard.press("D")
        elif key == QtCore.Qt.Key_E:
            self.vm.keyboard.press("E")
        elif key == QtCore.Qt.Key_F:
            self.vm.keyboard.press("F")
        event.accept()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            event.ignore()
            return
        key = event.key()
        if key == QtCore.Qt.Key_1:
            self.vm.keyboard.unpress("1")
        elif key == QtCore.Qt.Key_2:
            self.vm.keyboard.unpress("2")
        elif key == QtCore.Qt.Key_3:
            self.vm.keyboard.unpress("3")
        elif key == QtCore.Qt.Key_4:
            self.vm.keyboard.unpress("4")
        elif key == QtCore.Qt.Key_5:
            self.vm.keyboard.unpress("5")
        elif key == QtCore.Qt.Key_6:
            self.vm.keyboard.unpress("6")
        elif key == QtCore.Qt.Key_7:
            self.vm.keyboard.unpress("7")
        elif key == QtCore.Qt.Key_8:
            self.vm.keyboard.unpress("8")
        elif key == QtCore.Qt.Key_9:
            self.vm.keyboard.unpress("9")
        elif key == QtCore.Qt.Key_0:
            self.vm.keyboard.unpress("0")
        elif key == QtCore.Qt.Key_A:
            self.vm.keyboard.unpress("A")
        elif key == QtCore.Qt.Key_B:
            self.vm.keyboard.unpress("B")
        elif key == QtCore.Qt.Key_C:
            self.vm.keyboard.unpress("C")
        elif key == QtCore.Qt.Key_D:
            self.vm.keyboard.unpress("D")
        elif key == QtCore.Qt.Key_E:
            self.vm.keyboard.unpress("E")
        elif key == QtCore.Qt.Key_F:
            self.vm.keyboard.unpress("F")
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


