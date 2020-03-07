import sys
from WalkingPatternAnalyseTool import PdVisualization
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys, os, subprocess, time, shutil, signal
import atexit


from PyQt5 import Qt, QtCore


start_Left = 0
start_Right = 0
f1 = "frames_Left"
f2 = "frames_Right"
pro1 = None
pro2 = None


class VideoWindow(Qt.QGraphicsView):
    def __init__(self, viewWin, dirName, st, parent=None):
        Qt.QGraphicsView.__init__(self, parent)
        self.scene  = Qt.QGraphicsScene()
        self.grview = viewWin
        self.timer = Qt.QTimer(self)
        self.n = 0
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(100)
        self.grview.show()
        self.dirname = dirName
        self.start_control = st




    def on_timeout(self):
        self.listFiles = os.listdir(self.dirname)
        # print(len(self.listFiles))
        if self.start_control == 0:
            start = start_Left
        else:
            start = start_Right
        if start and len(self.listFiles)>0:
            # print("in", self.n)
            if self.n < len(self.listFiles):
                self.scene.clear()
                file = self.listFiles[self.n]
                pixmap = Qt.QPixmap(self.dirname +"\{}".format(file))
                self.scene.addPixmap(pixmap)
                self.grview.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
                self.grview.setScene(self.scene)
                self.n += 1
            else:
                print("end", self.dirname)
                self.timer.stop()


def startVis():
    print("start!")

    if os.path.exists(f1):
        shutil.rmtree(f1)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)
    os.makedirs(f2)

    global pro1, pro2, start_Left,start_Right
    pro1 = subprocess.Popen("blender -b untitled.blend -x 1 -o //"+f1+"/render -s 10 -e 50 -a",  stdout=subprocess.DEVNULL)
    pro2 = subprocess.Popen("blender -b untitled.blend -x 1 -o //"+f2+"/render -s 10 -e 50 -a",  stdout=subprocess.DEVNULL)

    time.sleep(5)

    start_Left = 1
    start_Right = 1


def exit_handler():
    if pro1 != None:
        time.sleep(0.1)
        pro1.kill()
    if pro2 != None:
        time.sleep(0.1)
        pro2.kill()

    if os.path.exists(f1):
        shutil.rmtree(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)


    print('My application is ending!')




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()


    if os.path.exists(f1):
        shutil.rmtree(f1)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)
    os.makedirs(f2)

    ui = PdVisualization.Ui_mainWindow()
    ui.setupUi(MainWindow)
    ui.graphicsView = VideoWindow( ui.graphicsView , f1 ,0)
    ui.graphicsView_2 = VideoWindow( ui.graphicsView_2 , f2 ,1)

    ui.pushButton.clicked.connect(startVis)

    MainWindow.show()

    atexit.register(exit_handler)
    sys.exit(app.exec_())



