import vtk
from numpy import random
import scipy.io
from vtk import vtkCommand





class VtkMovingObj:

    def __init__(self, initial_pos):
        reader = vtk.vtkSTLReader()
        reader.SetFileName("panter.stl")

        # source = vtk.vtkSphereSource()
        # source.SetRadius(3.0)
        cube = vtk.vtkCubeSource()
        cube.SetXLength(5)
        cube.SetYLength(4)
        cube.SetZLength(3)

        self.vtkPolyData = vtk.vtkPolyData()
        self.mapper = vtk.vtkPolyDataMapper()
        # self.mapper.SetInputConnection(reader.GetOutputPort())
        self.mapper.SetInputConnection(cube.GetOutputPort())

        
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(self.mapper)
        self.vtkActor.SetPosition( initial_pos )
        # self.vtkActor.SetScale(0.5,0.5,0.5)


        # adjust the position
        # translate(scale(translate(model, -P)), P)
        # transform = vtk.vtkTransform() 
        # transform.Translate( self.vtkActor.GetCenter())
        # transform.RotateX(-90)
        # transform.RotateZ(90)
        # transform.Scale(0.01, 0.01, 0.01)
        # self.vtkActor.SetUserTransform(transform)

    def changePosition(self, position):
        self.vtkActor.SetPosition( position )

    def getPos(self):
        return self.vtkActor.GetPosition()

   


class MoveFootTimerCallback():
    def __init__(self, renderer, movingObj, iterations, positions,movingObj2, position2 ):
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

        

    def execute(self, iren, event):
        if self.iterations == 0:
            self.movingObj.changePosition(self.positions[self.posCounter])
            self.movingObj2.changePosition(self.positions2[self.posCounter])

            self.iterations = 10
            self.posCounter += 1
            

            # if self.foot == "L" and self.posCounter < len(self.positions):
            self.renderer.ResetCamera()
            # self.cam.SetFocalPoint(  (self.positions[self.posCounter] + self.positions2[self.posCounter])/2 ) 
            self.camFoc = self.cam.GetFocalPoint()
            self.campos = self.cam.GetPosition()
            # self.cam.SetPosition(  self.campos - (0,0,0) )

        if self.posCounter == 0:
            self.renderer.ResetCamera()
            self.getCamPos()
           
        if self.posCounter == len(self.positions):
            iren.DestroyTimer(self.timerId)
            # self.points.SetNumberOfPoints(self.posCounter)
            # self.lines.InsertNextCell(self.posCounter )


        self.iterations -= 1

        self.renderer.SetActiveCamera(self.cam)


        self.renderer.AddActor(self.movingObj.vtkActor)
        self.renderer.AddActor(self.movingObj2.vtkActor)



        iren.GetRenderWindow().Render()
        
    def changeCamPos(self):
        self.cam.SetPosition(self.campos )
        self.cam.SetFocalPoint(self.camFoc  )
        #self.cam.SetViewUp()


    def getCamPos(self):
        self.cam = renderer.GetActiveCamera()
        self.campos = self.cam.GetPosition() 
        self.camFoc = self.cam.GetFocalPoint()
        

        
        


        #print(self.movingObj.getPos() )


def onLeftButtonPressEvent(sender, event):
    moveFootTimerCallback.getCamPos()
    moveFootTimerCallback.changeCamPos()

def onMouseWheelForwardEvent(sender, event):
    moveFootTimerCallback.getCamPos()
    moveFootTimerCallback.changeCamPos()

def onMouseWheelBackwardEvent(sender, event):
    moveFootTimerCallback.getCamPos()
    moveFootTimerCallback.changeCamPos()


if __name__ == "__main__":
    # Renderer
    renderer = vtk.vtkRenderer()
    #renderer.SetBackground(.2, .3, .4)
    renderer.ResetCamera()

    # Render Window
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)

    renderer.SetBackground(0.1, 0.2, 0.4)
    renderWindow.AddRenderer(renderer)




    # Interactor
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    # if change scene
    renderWindowInteractor.AddObserver(
        vtkCommand.LeftButtonPressEvent,
        onLeftButtonPressEvent)
    renderWindowInteractor.AddObserver(
        vtkCommand.MouseWheelForwardEvent,
        onMouseWheelForwardEvent)
    renderWindowInteractor.AddObserver(
        vtkCommand.MouseWheelBackwardEvent,
        onMouseWheelBackwardEvent)


    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderWindowInteractor.Initialize()

    

    # Initialize a timer for the animation

    mat = scipy.io.loadmat('../WalkingPositionData/linePos_3603_20191220.mat')['linPos']
    mat = mat[::10]

    mat2 = scipy.io.loadmat('../WalkingPositionData/linePos_3593_20191220-095327.mat')['linPos']
    mat2 = mat2[::10]
    

    left_foot = VtkMovingObj( mat[0])
    right_foot = VtkMovingObj( mat2[0])

    moveFootTimerCallback = MoveFootTimerCallback(renderer, left_foot, 100, mat, right_foot,mat2 )
    renderWindowInteractor.AddObserver('TimerEvent', moveFootTimerCallback.execute)
    timerId1 = renderWindowInteractor.CreateRepeatingTimer(10)
    moveFootTimerCallback.timerId = timerId1

    # moveFootTimerCallback2 = MoveFootTimerCallback(renderer, right_foot, 10, mat2,"R")
    # renderWindowInteractor.AddObserver('TimerEvent', moveFootTimerCallback2.execute)
    # # timerId2 = renderWindowInteractor.CreateRepeatingTimer(10)
    # moveFootTimerCallback2.timerId = timerId1

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()
    