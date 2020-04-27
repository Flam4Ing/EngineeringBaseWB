import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
global observer


class SelObserverEdgeToEdge:
    def __init__(self):
        self.createGUI()
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []

    def createGUI(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Align Edges")
        layout = QtGui.QGridLayout(self.form)
        self.InfoLabel = QtGui.QLabel()
        self.InfoLabel.setText("Select edge on First object!")
        layout.addWidget(self.InfoLabel, 0, 0)
        self.btnRotate = QtGui.QPushButton("Rotate 180")
        self.btnRotate.clicked.connect(self.Rotate_180)
        layout.addWidget(self.btnRotate, 1, 1)

    def Rotate_180(self):
        # new placement
        d = FreeCAD.Rotation
        self.angleToRotate.Angle
        new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), self.angleToRotate, self.center)
        # apply placement
        self.objA.Placement = new_plm.multiply(self.objA.Placement)

    def reject(self):
        RemoveObservers()
        FreeCADGui.Control.closeDialog()

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object

        if str(sub).startswith("Edge"):
            sel = FreeCAD.Gui.Selection.getSelectionEx()
            mainObj = sel[0].Object
            subObj = sel[0].SubObjects[0]
            self.stack.append([mainObj, subObj])
        if len(self.stack) == 1:
            self.InfoLabel.setText("Select edge on Second object")
        if len(self.stack) == 2:
            self.MoveObjects()

    def MoveObjects(self):
        FreeCAD.ActiveDocument.openTransaction("Align edges")
        self.objA = self.stack[0][0]
        edgeA = self.stack[0][1]
        edgeB = self.stack[1][1]
        # transform object A placement
        # edge vector
        edgeA_EndPoint = edgeA.lastVertex(True).Point
        edgeA_StartPoint = edgeA.firstVertex(True).Point
        edgeA_MidPoint = (edgeA_EndPoint + edgeA_StartPoint).multiply(0.5)
        edgeB_EndPoint = edgeB.lastVertex(True).Point
        edgeB_StartPoint = edgeB.firstVertex(True).Point
        edgeB_MidPoint = (edgeB_EndPoint + edgeB_StartPoint).multiply(0.5)
        va = (edgeA_EndPoint - edgeA_StartPoint).normalize()
        vb = (edgeB_EndPoint - edgeB_StartPoint).normalize()
        self.angleToRotate = FreeCAD.Rotation(va, vb)

        # rot centre
        # center = edgeA_StartPoint
        self.center = edgeA_MidPoint
        # new placement
        new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), self.angleToRotate, self.center)
        # apply placement
        self.objA.Placement = new_plm.multiply(self.objA.Placement)
        # laying on edge
        # distatceVector = edgeA_StartPoint - edgeB_StartPoint
        distatceVector = edgeA_MidPoint - edgeB_MidPoint
        MVector = self.objA.Placement.Base - distatceVector
        self.objA.Placement.Base = MVector
        FreeCAD.ActiveDocument.commitTransaction()

        print("First object -" + str(self.objA.Label) + "- is moved!")
        RemoveObservers()
        self.stack = []

def AlignEdges():
    global observer
    try:
        selGate = WBAuxiliaries.SelectionGate("Edge")
        FreeCADGui.Selection.addSelectionGate(selGate)
        observer = SelObserverEdgeToEdge()
        FreeCADGui.Selection.addObserver(observer)
        FreeCADGui.Control.showDialog(observer)
    except:
        RemoveObservers()

def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")

AlignEdges()