import sys
# from WalkingPatternAnalyseTool import PdVisualization
import PdVisualization
from RenderWindow import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QDialog,QLabel,QHBoxLayout,\
     QVBoxLayout, QDialogButtonBox
import sys, os, subprocess, time, shutil, signal
import atexit
import numpy as np
from PyQt5 import Qt, QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
import scipy.io as sio
import vtk

import vtk.qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# control start or stop for patient and HC, 0 for pause, 1 for start
start_Left = 0
start_Right = 0

# s1 = None
# s2 = None

# file name for file selected from left file browser (patient)
file_1 = None
# file name for file selected from right file browser(HC)
file_2 = None
file_for = 'P'   # file for patient or HC

rt = None   # repeat timer
K = 8       # use all data will be time consuming, get sliced data (read every every k data) 

fcode_left = "3603"   # the default file code for right foot signal in Sensor hdf5 file
fcode_right = "3593"   # the default file code for left foot signal in Sensor hdf5 file

# class used to update the GUI for walking pattern visualization 
class VideoWindow:
    def __init__(self, viewWin, st, slider, timeLabel, parent=None):
        # Qt.QVBoxLayout.__init__(self, parent)
        self.win = viewWin
        self.frame = Qt.QFrame()
        # get the RenderWindowInteractor from vtk window
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        # add the RenderWindowInteractor to the PyQt5 GUI
        self.win.addWidget(self.vtkWidget)
        self.vtkRen = vtkWin(self.vtkWidget, slider, timeLabel )

    def getWin(self):
        return self.win 


# class used to handle file browser, will create a popup window
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


# class used to show error dialog 
class CustomDialog(QDialog):

    def __init__(self, infotext, parent=None):
        QDialog.__init__(self, parent)

        self.setWindowTitle("Info Box")
        self.resize(150, 150)
        self.info = QLabel(infotext)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.info)
        self.layout.addWidget( self.buttonBox)
        self.setLayout(self.layout)



# class used to show signals (accelerations)
class SignalWindow:
    def __init__(self, viewWin, matdata, coresVideo, parent=None):
        # Qt.QGraphicsView.__init__(self, parent)
        # 1. Window settings
        self.grview = viewWin
        self.corresponding_video = coresVideo

        # 2. Place the matplotlib figure
        # Todo: x_len is the length of the data
        # Todo: y_range should be adjust itself, x should be change with timer, interval should be adjust with video
        self.myFig = []
        self.canvas_left =  MyFigureCanvas(fcode=fcode_left, x_len=30, y_range=[-1200, 1200], interval=20,
                                    signal_mat=matdata, video = self.corresponding_video )
        self.myFig.append(self.canvas_left)
        self.canvas_right = MyFigureCanvas(fcode=fcode_right, x_len=30, y_range=[-1200, 1200], interval=20,
                                    signal_mat=matdata, video = self.corresponding_video )
        self.myFig.append(self.canvas_right)


        self.layout = QHBoxLayout(self.grview)
        self.layout.addWidget(self.myFig[0])
        self.layout.addWidget(self.myFig[1])
        self.grview.setLayout(self.layout)

        # 3. Show
        # print(self.grview.mapToScene(self.grview.rect()).boundingRect())
        # self.grview.fitInView(self.grview.mapToScene(self.grview.rect()).boundingRect())
        self.grview.fitInView(0, 0, 115, 200)
        self.grview.show()
        return

    def getWin(self):
        return self.grview

class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self, fcode, x_len, y_range, interval, signal_mat, video):
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range
        self.interval = interval
        self.data = signal_mat['linAcc_'+fcode][::K]
        self.video = video
        self.t = 0
        self.video_t = self.video.moveFootTimerCallback.getPosCounter()

        # Store a figure and ax
        ax = self.figure.subplots() # plot 1 figure

        fcode = fcode

        if fcode == fcode_left:
            ax.set_title('Acceleration-Left', fontsize=7)
        else:
            ax.set_title('Acceleration-Right', fontsize=7)
        ax.set_xlabel('time [1/128s]', fontsize=7)
        ax.set_ylabel('Acceleration', fontsize=7, labelpad=5)
        ax.tick_params(labelsize=5)

        self._animat_axs_(ax)
        
        return



    def _animat_axs_(self, ax):
        ax.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        # Store two lists _x_ and _y_
        x = [[i,i,i] for i in range(0, self._x_len_) ]
        x = np.array(x)
        y = [[0 for i in range(3)] for j in range(0, self._x_len_)]
        y = np.array(y)


        self._lineX_, self._lineY_, self._lineZ_, = ax.plot(x[:,0].tolist(), y[:,0].tolist(), 'r',
                                                                   x[:,1].tolist(), y[:,1].tolist(), 'b',
                                                                   x[:,2].tolist(), y[:,2].tolist(), 'g')

        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y.tolist(), ),
                                  interval=self.interval, blit=True)
        return

    def _update_canvas_(self,i, y) -> None:
        '''
        This function gets called regularly by the timer.
        '''
        self.video_t = self.video.moveFootTimerCallback.getPosCounter()
        if self.t  !=  self.video_t:
            if abs(self.video_t - self.t) >= 100:
                self.t = self.video_t
                for j in range(0, self._x_len_ -1 ):
                    y.append([0,0,0])

            else:
                self.t = self.video_t
            y.append(self._get_next_datapoint( self.t )) # Add new datapoint
        y = y[-self._x_len_:]  # Truncate list _y_ : avoid broadcast error
        y = np.array(y)
        self._lineX_.set_ydata(y[:,0].tolist())
        self._lineY_.set_ydata(y[:,1].tolist())
        self._lineZ_.set_ydata(y[:,2].tolist())

        return self._lineX_, self._lineY_, self._lineZ_

    def _get_next_datapoint(self, i ):
        if i > len(self.data):
            print("signal end!")

        return self.data[i]


# function called when start visualization button is clicked 
def startVis():
    print("start!")

    global start_Left,start_Right, ui, file_1, file_2, rt,  v1, v2, s1, s2

    # error 1, no file is chosen 
    if file_1 == None or file_2 == None:
        d = CustomDialog("Please select data files before you start")
        d.exec_()
        return 

    try:
        dataMat = sio.loadmat( file_1 ) 
        dataMat2 = sio.loadmat( file_2 ) 
        mat1_left = dataMat['linPosHP_'+fcode_left][::K]
        mat1_right = dataMat['linPosHP_'+fcode_right][::K]
        mat2_left = dataMat2['linPosHP_'+fcode_left][::K]
        mat2_right = dataMat2['linPosHP_'+fcode_right][::K]
    except:
        # error 2: file chosen is not the file we got from matlab
        d = CustomDialog("Please use official tool to generate data file")
        d.exec_()
        return 

    # both patient and HC will start
    start_Left = 1
    start_Right = 1

    # send the data we read from mat files
    v1.vtkRen.setMat(mat1_left, mat1_right)
    v2.vtkRen.setMat(mat2_left, mat2_right)

    # update value for sliders
    ui.horizontalSlider.setMaximum( len(mat1_left)-1 )
    ui.horizontalSlider_HC.setMaximum( len(mat2_left)-1 )

    #update signals windows
    s1 = SignalWindow(viewWin=ui.graphicsView_3,
                                     matdata=dataMat, coresVideo = v1.vtkRen )
    s2 = SignalWindow(viewWin=ui.graphicsView_4,
                                     matdata=dataMat, coresVideo = v2.vtkRen)
    ui.graphicsView_3 = s1.getWin()
    ui.graphicsView_4 = s2.getWin()

    # create an overall control timer
    rt = RepeatedTimer(0.06, updateWins )

    

    


    
# function called by the repeated timer , will update the windows if it is not paused
def updateWins():
    global v1, v2, start_Left, start_Right
    if start_Left == 1:
        v1.vtkRen.moveFootTimerCallback.execute()
    if start_Right == 1:
        v2.vtkRen.moveFootTimerCallback.execute()


# exit handler
def exit_handler():
    print('My application is ending!')

# called when the value for left slider is changed
def leftSliderReleased():
    global  ui, v1
    v1.vtkRen.moveFootTimerCallback.posCounter = ui.horizontalSlider.value()

# called when the value for right slider is changed
def rightSliderReleased():
    global  ui, v2
    v2.vtkRen.moveFootTimerCallback.posCounter = ui.horizontalSlider_HC.value()


# called when start/pause button for patient is clicked
def pauseLeft():
    global start_Left, ui
    # if play, change to pause
    if start_Left == 1:
        start_Left = 0
    # if pause, change to play
    else:
        start_Left = 1

# called when start/pause button for HC is clicked
def pauseRight():
    global start_Right, ui
    # if play, change to pause
    if start_Right == 1:
        start_Right = 0
    # if pause, change to play
    else:
        start_Right = 1

# open file browser for patient
def openFiles_P():
    global file_for
    file_for = 'P'
    ex = FileWindow()

# open file browser for HC
def openFiles_HC():
    global file_for
    file_for = 'HC'
    ex = FileWindow()


if __name__ == '__main__':
    atexit.register(exit_handler)

    # initilaize PyQt main window 
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
    ui = PdVisualization.Ui_mainWindow()
    ui.setupUi(MainWindow)

    # link files browser button to corresponding handler 
    ui.btn_flist_1.clicked.connect( openFiles_P )
    ui.btn_flist_5.clicked.connect( openFiles_HC )

    # link vtk visualization window to the corresponding window in PyQt GUI
    v1 = VideoWindow( ui.vbox, 0, ui.horizontalSlider, ui.time_P)
    v2 = VideoWindow( ui.vbox_HC, 1, ui.horizontalSlider_HC, ui.time_HC)
    ui.graphicsView = v1.getWin()
    ui.graphicsView_2 = v2.getWin()

    # link start visualization button to corresponding function 
    ui.btn_start.clicked.connect(startVis)

    # link slider values to corresponding function 
    ui.horizontalSlider.sliderReleased.connect(leftSliderReleased)
    ui.horizontalSlider_HC.sliderReleased.connect(rightSliderReleased)

    # linke pause and play to corresponding function 
    ui.toolButton_pause.clicked.connect(pauseLeft)
    ui.toolButton_pause_HC.clicked.connect(pauseRight)

    
    MainWindow.show()

    
    k = app.exec_()
    # stop timer when exit the application 
    if k == 0:
        try:
            rt.stop()
        except:
            pass
    sys.exit(k)


