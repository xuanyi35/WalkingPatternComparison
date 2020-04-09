import vtk
from numpy import random
import scipy.io
from vtk import vtkCommand





class VtkMovingObj:

    def __init__(self, initial_pos):
        reader = vtk.vtkSTLReader()
        reader.SetFileName("Giratina.stl")

        self.vtkPolyData = vtk.vtkPolyData()
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        
        self.vtkActor = vtk.vtkActor()
        self.vtkActor.SetMapper(mapper)
        self.vtkActor.SetPosition( initial_pos )
        #self.vtkActor.SetScale(0.5,0.5,0.5)


        # adjust the position
        transform = vtk.vtkTransform() 
        transform.Translate(self.vtkActor.GetCenter())
        transform.RotateX(-90)
        self.vtkActor.SetUserTransform(transform)

    def changePosition(self, position):
        self.vtkActor.SetPosition( position )

    def getPos(self):
        return self.vtkActor.GetPosition()

   


class MoveFootTimerCallback():
    def __init__(self, renderer, movingObj, iterations, positions):
        self.iterations = iterations
        self.renderer = renderer
        self.cam = None
        self.campos = None
        self.camFoc = None
        self.movingObj = movingObj
        self.positions = positions
        self.posCounter = 0

    def execute(self, iren, event):
        if self.iterations == 0:
            self.movingObj.changePosition(self.positions[self.posCounter])
            self.iterations = 2
            self.posCounter += 1
            #self.campos += self.positions[self.posCounter]
            #self.camFoc += self.positions[self.posCounter] 

            # self.renderer.ResetCamera()
            # self.getCamPos()
            
        if self.posCounter == 0:
            self.renderer.ResetCamera()
            self.getCamPos()
           
        if self.posCounter == len(self.positions):
            iren.DestroyTimer(self.timerId)

        self.iterations -= 1

        self.renderer.SetActiveCamera(self.cam)
        self.renderer.AddActor( self.movingObj.vtkActor)       
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
    # Read the image
    # jpeg_reader = vtk.vtkJPEGReader()
    # if not jpeg_reader.CanReadFile('cat.jpg'):
    #     print("Error reading file %s" % 'cat.jpg')
        

    # Create a renderer to display the image in the background
    # background_renderer = vtk.vtkRenderer()
    # jpeg_reader.SetFileName('cat.jpg')
    # jpeg_reader.Update()
    # image_data = jpeg_reader.GetOutput()
    # Create an image actor to display the image
    # image_actor = vtk.vtkImageActor()
    # image_actor.SetInputData(image_data)


# Set up the render window and renderers such that there is
    # a background layer and a foreground layer
    # background_renderer.SetLayer(0)
    # background_renderer.InteractiveOff()
    # background_renderer.AddActor(image_actor)
    # renderer.SetLayer(1)
    # renderWindow.SetNumberOfLayers(2)
    # renderWindow.AddRenderer(background_renderer)
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
    # mat = scipy.io.loadmat('disp.mat')['linPosHP']
    mat = scipy.io.loadmat('../WalkingPositionData/linePos_3603_20191220.mat')['linPos']
    

    print(mat)
    points = vtk.vtkPoints()
    points.SetNumberOfPoints(len(mat))
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(len(mat))

    for i in range(len(mat)):
        points.SetPoint(i, mat[i][0],mat[i][1],mat[i][2])
        lines.InsertCellPoint(i)
    polygon = vtk.vtkPolyData()
    polygon.SetPoints(points)
    polygon.SetLines(lines)
    polygonMapper = vtk.vtkPolyDataMapper()
    polygonMapper.SetInputData(polygon)
    polygonMapper.Update()
    polygonActor = vtk.vtkActor()
    polygonActor.SetMapper(polygonMapper)
    renderer.AddActor(polygonActor)




    people = VtkMovingObj( mat[0])
    moveFootTimerCallback = MoveFootTimerCallback(renderer,people, 2, mat)
    renderWindowInteractor.AddObserver('TimerEvent', moveFootTimerCallback.execute)
    timerId = renderWindowInteractor.CreateRepeatingTimer(10)
    moveFootTimerCallback.timerId = timerId

    # Begin Interaction
    renderWindow.Render()
    renderWindowInteractor.Start()
    