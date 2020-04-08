import sys
from WalkingPatternAnalyseTool import PdVisualization
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QDialog,QLabel, QVBoxLayout, QDialogButtonBox
import sys, os, subprocess, time, shutil, signal
import atexit
import numpy as np
from PyQt5 import Qt, QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib as mpl
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim
# from matplotlib.backends.qt_compat import QtCore, QtWidgets

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

file_1 = None
file_2 = None
file_for = 'P'   # file for patient or HC

class VideoWindow(Qt.QGraphicsView):
    def __init__(self, viewWin, dirName, st, slider, parent=None):
        Qt.QGraphicsView.__init__(self, parent)
        self.scene  = Qt.QGraphicsScene()
        self.grview = viewWin
        self.timer = Qt.QTimer(self)
        self.n = 0
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(300)
        self.grview.show()
        self.dirname = dirName
        self.st = st
        self.slider = slider


    def on_timeout(self):
        global t1, t2
        self.listFiles = os.listdir(self.dirname)
        t = 0
        # print(len(self.listFiles))
        if self.st == 0:
            start = start_Left
            self.n = t1
        else:
            start = start_Right
            self.n = t2
        if start and len(self.listFiles)>0:
            # print("in", self.n)
            if self.n < len(self.listFiles):
                self.scene.clear()
                file = self.listFiles[self.n]
                pixmap = Qt.QPixmap(self.dirname +"\{}".format(file))
                self.scene.addPixmap(pixmap)
                self.grview.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
                self.grview.setScene(self.scene)
                self.slider.setValue(self.n)
                self.n += 1
                if self.st == 0:
                    t1 = self.n
                else:
                    t2 = self.n
            elif self.n >= len(self.listFiles):
                self.scene.clear()
                pixmap = Qt.QPixmap('wait.png')
                self.scene.addPixmap(pixmap)
                self.grview.fitInView(self.scene.itemsBoundingRect())
                self.grview.setScene(self.scene)
                self.slider.setValue(self.n)
                print("wait", self.dirname)
                if self.n == len(self.listFiles):
                    time.sleep(2)
                # self.timer.stop()


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
            ui.patient_file.setPlainText(fileName)
            file_1 = fileName
        else:
            file_2 = fileName
            ui.HC_file.setPlainText(fileName)


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
    def __init__(self, viewWin, parent=None):
        Qt.QGraphicsView.__init__(self, parent)
        # 1. Window settings
        self.grview = viewWin
        self.scene = Qt.QGraphicsScene()
        print(viewWin.rect())

        # 2. Place the matplotlib figure
        self.myFig = MyFigureCanvas(x_len=200, y_range=[0, 100], interval=20)
        self.scene.addWidget(self.myFig )
        # self.scene.setSceneRect(QtCore.QRectF(viewWin.rect()))

        self.grview.fitInView(self.scene.itemsBoundingRect())

        self.grview.setScene(self.scene)

        # 3. Show
        self.grview.show()
        return

class MyFigureCanvas(FigureCanvas, anim.FuncAnimation):
    '''
    This is the FigureCanvas in which the live plot is drawn.

    '''

    def __init__(self, x_len, y_range, interval):
        '''
        :param x_len:       The nr of data points shown in one plot.
        :param y_range:     Range on y-axis.
        :param interval:    Get a new datapoint every .. milliseconds.

        '''
        FigureCanvas.__init__(self, mpl_fig.Figure())
        # Range settings
        self._x_len_ = x_len
        self._y_range_ = y_range

        # Store two lists _x_ and _y_
        x = list(range(0, x_len))
        y = [0] * x_len

        # Store a figure and ax
        self._ax_ = self.figure.subplots()
        self._ax_.set_ylim(ymin=self._y_range_[0], ymax=self._y_range_[1])
        self._line_, = self._ax_.plot(x, y)

        # Call superclass constructors
        anim.FuncAnimation.__init__(self, self.figure, self._update_canvas_, fargs=(y,), interval=interval,
                                    blit=True)
        return

    def _update_canvas_(self, i, y) -> None:
        '''
        This function gets called regularly by the timer.

        '''
        y.append(round(get_next_datapoint(), 2))  # Add new datapoint
        y = y[-self._x_len_:]  # Truncate list _y_
        self._line_.set_ydata(y)
        return self._line_,


def startVis():
    print("start!")


    if os.path.exists(f1):
        shutil.rmtree(f1)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2)
    os.makedirs(f2)

    global pro1, pro2, start_Left,start_Right, ui, file_1, file_2

    print(file_1)
    print(file_2)

    pro1 = subprocess.Popen("blender -b untitled.blend -x 1 -o //"+f1+"/render -s 10 -e 500 -a",  stdout=subprocess.DEVNULL)
    pro2 = subprocess.Popen("blender -b untitled2.blend -x 1 -o //"+f2+"/render -s 10 -e 500 -a",  stdout=subprocess.DEVNULL)
    ui.horizontalSlider.setMaximum(490)
    ui.horizontalSlider_2.setMaximum(490)

    # wait for 7 seconds and close
    d = CustomDialog()
    QtCore.QTimer.singleShot(7000, d.close )
    d.exec_()


    start_Left = 1
    start_Right = 1


def exit_handler():
    global pro1, pro2
    try:
        pro1.kill()
        pro2.kill()
    except:
        pass
    # if pro1 != None:
    #     time.sleep(0.1)
    #     pro1.kill()
    # if pro2 != None:
    #     time.sleep(0.1)
    #     pro2.kill()

    if os.path.exists(f1):
        shutil.rmtree(f1, ignore_errors=True)
    if os.path.exists(f2):
        shutil.rmtree(f2, ignore_errors=True)


    print('My application is ending!')



def leftSliderReleased():
    global t1, ui
    t1 = ui.horizontalSlider.value()


def rightSliderReleased():
    global t2, ui
    t2 = ui.horizontalSlider_2.value()


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
n = np.linspace(0, 499, 500)
d = 50 + 25 * (np.sin(n / 8.3)) + 10 * (np.sin(n / 7.5)) - 5 * (np.sin(n / 1.5))
i = 0
def get_next_datapoint():
    global i
    i += 1
    if i > 499:
        i = 0
    return d[i]



if __name__ == '__main__':

    if os.path.exists(f1):
        shutil.rmtree(f1, ignore_errors=True)
    os.makedirs(f1)
    if os.path.exists(f2):
        shutil.rmtree(f2, ignore_errors=True)
    os.makedirs(f2)

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()



    ui = PdVisualization.Ui_mainWindow()
    ui.setupUi(MainWindow)
    # choose files
    ui.patient_btn.clicked.connect( openFiles_P )
    ui.HC_btn.clicked.connect( openFiles_HC )

    # visualization window
    ui.graphicsView = VideoWindow( ui.graphicsView, f1, 0, ui.horizontalSlider)
    ui.graphicsView_2 = VideoWindow( ui.graphicsView_2, f2, 1, ui.horizontalSlider_2)

    #  start visualization
    ui.pushButton.clicked.connect(startVis)

    # read slider value
    ui.horizontalSlider.sliderReleased.connect(leftSliderReleased)
    ui.horizontalSlider_2.sliderReleased.connect(rightSliderReleased)

    # pause and release
    ui.toolButton_5.clicked.connect(pauseLeft)
    ui.toolButton_8.clicked.connect(pauseRight)

    #signals window
    ui.graphicsView_3 = SignalWindow(ui.graphicsView_3)



    MainWindow.show()

    atexit.register(exit_handler)
    sys.exit(app.exec_())


