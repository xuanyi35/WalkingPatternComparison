import vtk, time
from numpy import random
import scipy.io
from vtk import vtkCommand
from PyQt5.QtCore import QTimer
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from threading import Timer
import threading


class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class VtkMovingObj:

    def __init__(self, initial_pos, is_right):
        # source = vtk.vtkSphereSource()
        # source.SetRadius(3.0)
        # cube = vtk.vtkCubeSource()
        # cube.SetXLength(5)
        # cube.SetYLength(4)
        # cube.SetZLength(3)
        self.reader = vtk.vtkOBJReader()
        self.reader.SetFileName("shoes.obj")

        self.vtkPolyData = vtk.vtkPolyData()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.reader.GetOutputPort())

        
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.mapper)

        self.vtkActor.SetPosition( initial_pos )
        if(is_right):
            self.vtkActor.SetScale(0.005)
            self.vtkActor.RotateZ(90)
        else:
            self.vtkActor.SetScale(-0.005)
            self.vtkActor.RotateZ(90)
            self.vtkActor.RotateX(180)


    def changePosition(self, position):
        self.vtkActor.SetPosition( position )

    def getPos(self):
        return self.vtkActor.GetPosition()

   


class MoveFootTimerCallback():
    def __init__(self, renderer, movingObj, iterations, positions,movingObj2, position2, iren, slider ):
        self.iterations = iterations
        self.renderer = renderer
        self.cam = None
        self.campos = None
        self.camFoc = None
        self.movingObj = movingObj
        self.positions = positions
        self.posCounter = 0
        self.movingObj2 = movingObj2
        self.positions2 = position2
        self.i = 0
        self.iren = iren
        self.slider = slider

        

    # def execute(self, iren, event):
    def execute(self):
        # print(self.posCounter)
        # print(self.i)

        if self.posCounter == 0:
            self.renderer.ResetCamera()
            self.getCamPos()
           
        if self.posCounter == len(self.positions) -1 :
            self.posCounter -= 1

        if self.posCounter % 128 == 0:
            self.slider.setValue(self.posCounter)

        if self.i == self.iterations:
            self.movingObj.changePosition(self.positions[self.posCounter])
            self.movingObj2.changePosition(self.positions2[self.posCounter])
            self.i = 0
            self.posCounter += 1
            self.renderer.ResetCamera()
            self.camFoc = self.cam.GetFocalPoint()
            self.campos = self.cam.GetPosition()

        


        self.i += 1
        self.renderer.SetActiveCamera(self.cam)
        self.renderer.AddActor(self.movingObj.vtkActor)
        self.renderer.AddActor(self.movingObj2.vtkActor)

        # iren.GetRenderWindow().Render()
        self.iren.Render()

    def changeCamPos(self):
        self.cam.SetPosition(self.campos )
        self.cam.SetFocalPoint(self.camFoc  )
        #self.cam.SetViewUp()


    def getCamPos(self):
        self.cam = self.renderer.GetActiveCamera()
        self.campos = self.cam.GetPosition() 
        self.camFoc = self.cam.GetFocalPoint()

    def getPosCounter(self):
        return self.posCounter
        

        
        


        #print(self.movingObj.getPos() )


# def onLeftButtonPressEvent(sender, event):
#     global moveFootTimerCallback
#     moveFootTimerCallback.getCamPos()
#     moveFootTimerCallback.changeCamPos()

# def onMouseWheelForwardEvent(sender, event):
#     global moveFootTimerCallback
#     moveFootTimerCallback.getCamPos()
#     moveFootTimerCallback.changeCamPos()

# def onMouseWheelBackwardEvent(sender, event):
#     global moveFootTimerCallback
#     moveFootTimerCallback.getCamPos()
#     moveFootTimerCallback.changeCamPos()

class vtkWin:
    def __init__(self, renderInter, slider):
        # Renderer
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(0.1, 0.2, 0.4)
        self.renderWindowInteractor = renderInter
        self.renderWindowInteractor.GetRenderWindow().AddRenderer(self.ren)
        self.renderWindowInteractor.Initialize()

        # initialize two foot 
        self.mat = [[0,0,0]]
        self.mat2 = [[0,0,0]]
        self.left_foot = VtkMovingObj( self.mat[0], 0)
        self.right_foot = VtkMovingObj( self.mat2[0], 1)
        self.slider = slider
        
        self.moveFootTimerCallback = MoveFootTimerCallback(self.ren, self.left_foot, 10, self.mat, self.right_foot, self.mat2, self.renderWindowInteractor, self.slider )

        

        self.renderWindowInteractor.Initialize()
        self.renderWindowInteractor.Start()


    def setMat(self, mat_left, mat_right):
        
        self.mat = mat_left[::1]
        self.mat2 = mat_right[::1]
        self.moveFootTimerCallback = MoveFootTimerCallback(self.ren, self.left_foot, 1, self.mat, self.right_foot, self.mat2, self.renderWindowInteractor, self.slider )
    

    

    
    
    
# if __name__ == "__main__":
#     # Render Window
#     renderWindow = vtk.vtkRenderWindow()
#     # renderWindow.SetSize(800, 800)
#     vtkWin(renderWindow)