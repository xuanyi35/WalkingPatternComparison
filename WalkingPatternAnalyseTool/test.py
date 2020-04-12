# import sys
# import vtk
# from PyQt5 import QtCore, QtGui
# from PyQt5 import Qt

# from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# class MainWindow(Qt.QMainWindow):

#     def __init__(self, parent = None):
#         Qt.QMainWindow.__init__(self, parent)

#         self.frame = Qt.QFrame()
#         self.vl = Qt.QVBoxLayout()
#         self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
#         self.vl.addWidget(self.vtkWidget)

#         self.ren = vtk.vtkRenderer()
#         self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
#         self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

#         # Create source
#         source = vtk.vtkSphereSource()
#         source.SetCenter(0, 0, 0)
#         source.SetRadius(5.0)

#         # Create a mapper
#         mapper = vtk.vtkPolyDataMapper()
#         mapper.SetInputConnection(source.GetOutputPort())

#         # Create an actor
#         actor = vtk.vtkActor()
#         actor.SetMapper(mapper)

#         self.ren.AddActor(actor)

#         self.ren.ResetCamera()

#         self.frame.setLayout(self.vl)
#         self.setCentralWidget(self.frame)

#         self.show()
#         self.iren.Initialize()
#         self.iren.Start()


# if __name__ == "__main__":
#     app = Qt.QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())


# import scipy.io as sio

# file_1 = "C:/Users/Cecilia/Desktop/804GUI/WalkingPatternComparison/WalkingPositionData/summary_20181012-102913_MLK_Walk.mat"

# dataMat = sio.loadmat( file_1 ) ['linPosHP_3603']
# print(len(dataMat))


print( '%02d:%02d'%(1, 2) )
