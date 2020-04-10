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

    def __init__(self, initial_pos):
        # source = vtk.vtkSphereSource()
        # source.SetRadius(3.0)
        cube = vtk.vtkCubeSource()
        cube.SetXLength(5)
        cube.SetYLength(4)
        cube.SetZLength(3)

        self.vtkPolyData = vtk.vtkPolyData()
        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(cube.GetOutputPort())

        
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.mapper)
        self.vtkActor.SetPosition( initial_pos )
      

    def changePosition(self, position):
        self.vtkActor.SetPosition( position )

    def getPos(self):
        return self.vtkActor.GetPosition()

   


class MoveFootTimerCallback():
    def __init__(self, renderer, movingObj, iterations, positions,movingObj2, position2, iren ):
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

        

    # def execute(self, iren, event):
    def execute(self):
        # print(self.posCounter)
        # print(self.i)
        if self.i == self.iterations:
            self.movingObj.changePosition(self.positions[self.posCounter])
            self.movingObj2.changePosition(self.positions2[self.posCounter])
            self.i = 0
            self.posCounter += 1
            self.renderer.ResetCamera()
            self.camFoc = self.cam.GetFocalPoint()
            self.campos = self.cam.GetPosition()

        if self.posCounter == 0:
            self.renderer.ResetCamera()
            self.getCamPos()
           
        if self.posCounter == len(self.positions):
            iren.DestroyTimer(self.timerId)
            # self.points.SetNumberOfPoints(self.posCounter)
            # self.lines.InsertNextCell(self.posCounter )


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
    def __init__(self, renderInter):
        # Renderer
        self.ren = vtk.vtkRenderer()
        # self.ren.ResetCamera()

        # renderWindow.AddRenderer(self.ren)
        self.ren.SetBackground(0.1, 0.2, 0.4)


        # Interactor
        # renderWindowInteractor = vtk.vtkRenderWindowInteractor()

        self.renderWindowInteractor = renderInter

        # self.renderWindowInteractor = QVTKRenderWindowInteractor(renderInter)

        # if change scene
        # self.renderWindowInteractor.AddObserver(
        #     vtkCommand.LeftButtonPressEvent,
        #     onLeftButtonPressEvent)
        # self.renderWindowInteractor.AddObserver(
        #     vtkCommand.MouseWheelForwardEvent,
        #     onMouseWheelForwardEvent)
        # self.renderWindowInteractor.AddObserver(
        #     vtkCommand.MouseWheelBackwardEvent,
        #     onMouseWheelBackwardEvent)


        self.renderWindowInteractor.GetRenderWindow().AddRenderer(self.ren)
        # renderWindowInteractor.SetRenderWindow(renderWindow)
        self.renderWindowInteractor.Initialize()

        

        # Initialize a timer for the animation

        self.mat = scipy.io.loadmat('../WalkingPositionData/linePos_3603_20191220.mat')['linPos']
        self.mat = self.mat[::10]

        self.mat2 = scipy.io.loadmat('../WalkingPositionData/linePos_3593_20191220-095327.mat')['linPos']
        self.mat2 = self.mat2[::10]
        

        self.left_foot = VtkMovingObj( self.mat[0])
        self.right_foot = VtkMovingObj( self.mat2[0])

        self.moveFootTimerCallback = MoveFootTimerCallback(self.ren, self.left_foot, 10, self.mat, self.right_foot, self.mat2, self.renderWindowInteractor )
        # self.renderWindowInteractor.AddObserver('TimerEvent', self.moveFootTimerCallback.execute)
        # self.renderWindowInteractor.CreateRepeatingTimer(1)
        # self.rt = RepeatedTimer(0.001, self.moveFootTimerCallback.execute )


        self.renderWindowInteractor.Initialize()
        self.renderWindowInteractor.Start()
    

    
    
    
# if __name__ == "__main__":
#     # Render Window
#     renderWindow = vtk.vtkRenderWindow()
#     # renderWindow.SetSize(800, 800)
#     vtkWin(renderWindow)