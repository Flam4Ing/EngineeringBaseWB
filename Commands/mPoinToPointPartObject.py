import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
global selObject

class SelObserverPointToPoint:
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        # print("Please select point on first object!")
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Move Part Object Point to Point")
        layout = QtGui.QGridLayout(self.form)
        self.InfoLabel = QtGui.QLabel()
        self.InfoLabel.setText("Select point on First object!")
        layout.addWidget(self.InfoLabel, 0, 0)
        self.btnXYZ = QtGui.QPushButton("Move XYZ")
        self.btnXYZ.clicked.connect(self.MoveXYZ)
        self.btnXYZ.setVisible(False)
        layout.addWidget(self.btnXYZ, 1, 1)
        self.btnX = QtGui.QPushButton("Move X")
        self.btnX.clicked.connect(self.MoveXYZ)
        self.btnX.setVisible(False)
        layout.addWidget(self.btnX, 1, 0)
        self.btnY = QtGui.QPushButton("Move Y")
        self.btnY.clicked.connect(self.MoveXYZ)
        self.btnY.setVisible(False)
        layout.addWidget(self.btnY, 2, 0)
        self.btnZ = QtGui.QPushButton("Move Z")
        self.btnZ.setVisible(False)
        self.btnZ.clicked.connect(self.MoveXYZ)
        layout.addWidget(self.btnZ, 3, 0)

    def reject(self):
        RemoveObservers()
        FreeCADGui.Control.closeDialog()

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
        global selObject
        if str(sub).startswith("Vertex"):
            objPoint = FreeCAD.Vector(pnt[0], pnt[1], pnt[2])
            self.stack.append([str(obj), objPoint])
        if len(self.stack) == 1:
            self.InfoLabel.setText("Select point on Second object!")
        if len(self.stack) == 2:
            ObjA_Name = self.stack[0][0]
            ObjB_Name = self.stack[1][0]
            PointA = self.stack[0][1]
            PointB = self.stack[1][1]
            Vector = PointB - PointA
            Pos0 = selObject.Placement.Base
            Rot0 = selObject.Placement.Rotation
            # Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation
            self.MVector = Pos0 + Vector
            # FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement = FreeCAD.Placement(MVector, Rot0)
            self.InfoLabel.setText("Move object!")
            self.btnXYZ.setVisible(True)
            self.btnX.setVisible(True)
            self.btnY.setVisible(True)
            self.btnZ.setVisible(True)

    def MoveXYZ(self):
        FreeCAD.ActiveDocument.openTransaction("Move Object")
        selObject.Placement.Base = self.MVector
        print("First object -" + selObject.Name + "- is moved!")
        FreeCAD.ActiveDocument.commitTransaction()
        RemoveObservers()
        self.stack = []
        FreeCADGui.Control.closeDialog()

try:
    selection = FreeCADGui.Selection.getSelectionEx()

    if len(selection) == 1 and selection[0].Object.isDerivedFrom('App::Part'):
        selObject = selection[0].Object
        FreeCADGui.Selection.clearSelection()
        selGate = WBAuxiliaries.SelectionGate("Vertex")
        FreeCADGui.Selection.addSelectionGate(selGate)
        observer = SelObserverPointToPoint()
        FreeCADGui.Selection.addObserver(observer)
        print(selObject.Name + " - is selected!")
        FreeCADGui.Control.showDialog(observer)
    else:
        WBAuxiliaries.MsgDialog("Please first select one Part Object!")

except:
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print("Observers are removed!")

def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")
