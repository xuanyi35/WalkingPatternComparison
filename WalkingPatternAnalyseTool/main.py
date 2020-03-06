import sys
from WalkingPatternAnalyseTool import PdVisualization
from PyQt5.QtWidgets import QApplication, QMainWindow

import os
import sys


from PyQt5 import Qt, QtCore
start = 1

class LeftWindow(Qt.QGraphicsView):
    def __init__(self, viewWin, parent=None):
        Qt.QGraphicsView.__init__(self, parent)
        self.scene  = Qt.QGraphicsScene()
        self.grview = viewWin
        dir = "frames"
        self.listFiles = os.listdir(dir)
        self.timer = Qt.QTimer(self)
        self.n = 0
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(100)
        self.grview.show()

    def on_timeout(self):
        if start :
            if self.n < len(self.listFiles):
                self.scene.clear()
                file = self.listFiles[self.n]
                pixmap = Qt.QPixmap("frames\{}".format(file))    # !!!  "frames\{}"
                self.scene.addPixmap(pixmap)
                self.grview.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

                self.grview.setScene(self.scene)                 # !!! (self.scene)
                self.n += 1
            else:
                self.timer.stop()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()



    ui = PdVisualization.Ui_mainWindow()
    ui.setupUi(MainWindow)
    ui.graphicsView = LeftWindow( ui.graphicsView )

    MainWindow.show()
    sys.exit(app.exec_())