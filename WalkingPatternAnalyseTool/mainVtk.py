import sys
# from WalkingPatternAnalyseTool import PdVisualization
import PdVisualization
from RenderWindow import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QDialog,QLabel, QVBoxLayout, QDialogButtonBox
import sys, os, subprocess, time, shutil, signal
import atexit
import numpy as np
from PyQt5 import Qt, QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
# from matplotlib.backends.qt_compat import QtCore, QtWidgets
import scipy.io as sio
import vtk

import vtk.qt
# vtk.qt.QVTKRWIBase = "QGLWidget"
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# control start or stop for left and right
start_Left = 0
start_Right = 0
# folder to save frames
f1 = "frames_Left"
f2 = "frames_Right"
# process to control left, right
pro1 = None
pro2 = None
# timer to link the slider
# horizontalSlider_2
t1 = 0
t2 = 0

i = 0

file_1 = None
file_2 = None
file_for = 'P'   # file for patient or HC
rt = None

class VideoWindow:
    def __init__(self, viewWin, dirName, st, slider, parent=None):
        # Qt.QVBoxLayout.__init__(self, parent)
        self.win = viewWin
        self.frame = Qt.QFrame()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.win.addWidget(self.vtkWidget)
        self.vtkRen = vtkWin(self.vtkWidget)

    def getWin(self):
        return self.win 

    # def stopTimer(self):
    #     self.vtkRen.rt.stop()


class FileWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Choose file dialogs'
        self.left = 100
        self.top = 100
        self.width = 720
        self.height = 560
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.close()


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        global file_for, file_1, file_2, ui
        if file_for == 'P' :
            ui.entry_flist_1.setPlainText(fileName)
            file_1 = fileName
        else:
            file_2 = fileName
            ui.entry_flist_5.setPlainText(fileName)


class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Info Box")
        self.resize(150, 150)
        self.info = QLabel("Wait, we are generating data.....")
        # QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        # self.buttonBox = QDialogButtonBox(QBtn)
        # self.buttonBox.accepted.connect(self.accept)
        # self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.info)
        # self.layout.addWidget( self.buttonBox)
        self.setLayout(self.layout)




class SignalWindow(Qt.QGraphicsView):
    def __init__(self, viewWin, signal_dir, parent=None):
        Qt.QGraphicsView.__init__(self, parent)
        # 1. Window settings
        self.grview = viewWin
        self.signal_dir = signal_dir
        self.scene = Qt.QGraphicsScene()
        # print(viewWin.rect())

        # 2. Place the matplotlib figure
        # Todo: x_len is the length of the data
        # Todo: y_range should be adjust itself, x should be change with timer, interval should be adjust with video
        self.myFig = MyFigureCanvas(x_len=300, y_range=[-800, 800], interval=20, signal_dir=self.signal_dir )
        self.scene.addWidget(self.myFig )
        # self.scene.setSceneRect(QtCore.QRectF(viewWin.rect()))
        # self.grview.fitInView(self.scene.itemsBoundingRect())

        self.grview.setScene(self.scene)

        # 3. Show
        # print(self.grview.mapToScene(self.grview.rect()).boundingRect())
        # self.grview.fitInView(self.grview.mapToScene(self.grview.rect()).boundingRect())
        self.grview.fitInView(0, 0, 200, 100)
        self.grview.show()
        return

class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self, x_len, y_range, interval, signal_dir):
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range
        self.signal_dir = signal_dir
        self.data = sio.loadmat(self.signal_dir)

        # Store two lists _x_ and _y_
        x = [[i,i,i] for i in range(0, x_len) ]
        x = np.array(x)
        y = [[0 for i in range(3)] for j in range(0, x_len)]
        y = np.array(y)

        # Store a figure and ax
        self._ax_ = self.figure.subplots() # plot 1 figure
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])

        self._lineX_, self._lineY_, self._lineZ_, = self._ax_.plot(x[:,0].tolist(), y[:,0].tolist(), 'r--',
                                                                   x[:,1].tolist(), y[:,1].tolist(), 'b--',
                                                                   x[:,2].tolist(), y[:,2].tolist(), 'g--')

        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y.tolist(),), interval=interval, blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        # y.append(round(self._get_next_datapoint(), 5))  # Add new datapoint
        y.append(self._get_next_datapoint()) # Add new datapoint
        y = y[-self._x_len_:]  # Truncate list _y_ : avoid broadcast error

        y = np.array(y)
        self._lineX_.set_ydata(y[:,0].tolist())
        self._lineY_.set_ydata(y[:,1].tolist())
        self._lineZ_.set_ydata(y[:,2].tolist())

        return self._lineX_, self._lineY_, self._lineZ_

    def _get_next_datapoint(self):
        global i
        i += 1
        if i > len(self.data['linAcc_3593'])-1:
            print("signal end!")

        return self.data['linAcc_3593'][i]



def startVis():
    print("start!")


    # if os.path.exists(f1):
    #     shutil.rmtree(f1)
    # os.makedirs(f1)
    # if os.path.exists(f2):
    #     shutil.rmtree(f2)
    # os.makedirs(f2)

    global pro1, pro2, start_Left,start_Right, ui, file_1, file_2

    print(file_1)
    print(file_2)

    #pro1 = subprocess.Popen("blender -b untitled.blend -x 1 -o //"+f1+"/render -s 10 -e 500 -a",  stdout=subprocess.DEVNULL)
    # pro2 = subprocess.Popen("blender -b untitled2.blend -x 1 -o //"+f2+"/render -s 10 -e 500 -a",  stdout=subprocess.DEVNULL)
    ui.horizontalSlider.setMaximum(490)
    ui.horizontalSlider_HC.setMaximum(490)

    # wait for 7 seconds and close
    # d = CustomDialog()
    # QtCore.QTimer.singleShot(7000, d.close )
    # d.exec_()


    start_Left = 1
    start_Right = 1
    global rt 
    rt = RepeatedTimer(0.001, updateWins )

def updateWins():
    global v1, v2
    v1.vtkRen.moveFootTimerCallback.execute()
    v2.vtkRen.moveFootTimerCallback.execute()


def exit_handler():
    print('My application is ending!')


def leftSliderReleased():
    global t1, ui
    t1 = ui.horizontalSlider.value()


def rightSliderReleased():
    global t2, ui
    t2 = ui.horizontalSlider_HC.value()


def pauseLeft():
    print("inLeft")
    global start_Left, ui
    if start_Left == 1:
        start_Left = 0
    else:
        start_Left = 1


def pauseRight():
    print("inRight")
    global start_Right, ui
    if start_Right == 1:
        start_Right = 0
    else:
        start_Right = 1


def openFiles_P():
    global file_for
    file_for = 'P'
    ex = FileWindow()

def openFiles_HC():
    global file_for
    file_for = 'HC'
    ex = FileWindow()



# Data source
# ------------
# n = np.linspace(0, 499, 500)
# d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))
# i = 0
# def get_next_datapoint_test():
#     global i
#     i += 1
#     if i > 499:
#         i = 0
#     return d[i]



if __name__ == '__main__':

    atexit.register(exit_handler)

    if os.path.exists(f1):
        shutil.rmtree(f1, ignore_errors=True)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2, ignore_errors=True)
    os.makedirs(f2)

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

    ui = PdVisualization.Ui_mainWindow()
    ui.setupUi(MainWindow)
    # choose files
    ui.btn_flist_1.clicked.connect( openFiles_P )
    ui.btn_flist_5.clicked.connect( openFiles_HC )

    # visualization window
    v1 = VideoWindow( ui.vbox, f1, 0, ui.horizontalSlider)
    v2 = VideoWindow( ui.vbox_HC, f2, 1, ui.horizontalSlider_HC)
    ui.graphicsView = v1.getWin()
    ui.graphicsView_2 = v2.getWin()

    #  start visualization
    ui.btn_start.clicked.connect(startVis)

    # read slider value
    ui.horizontalSlider.sliderReleased.connect(leftSliderReleased)
    ui.horizontalSlider_HC.sliderReleased.connect(rightSliderReleased)

    # pause and release
    ui.toolButton_pause.clicked.connect(pauseLeft)
    ui.toolButton_pause_HC.clicked.connect(pauseRight)

    #signals window
    ui.graphicsView_3 = SignalWindow(viewWin=ui.graphicsView_3,
                                     signal_dir="../WalkingPositionData/summary_20181012-102913_MLK_Walk.mat")
    ui.graphicsView_4 = SignalWindow(viewWin=ui.graphicsView_4,
                                     signal_dir="../WalkingPositionData/summary_20191220-095327_MLK_Walk.mat")


    MainWindow.show()

    
    k = app.exec_()
    if k == 0:
        # v1.stopTimer()
        # v2.stopTimer()
        try:
            rt.stop()
        except:
            pass
    sys.exit(k)


