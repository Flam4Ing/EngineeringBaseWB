import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
import  traceback
from Utils.EB_Geometry import *

global observer

class SelObserverPointToPoint:
    def __init__(self):
        self.createGUI()
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        self.toggle = 0

    def createGUI(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Move Part Object Point to Point")
        layout = QtGui.QGridLayout(self.form)
        #
        self.lblPromt = QtGui.QLabel()
        self.lblPromt.setText("Select point on First object!")
        layout.addWidget(self.lblPromt, 0, 0)
        #
        self.btnXYZ = QtGui.QPushButton("Move XYZ")
        self.btnXYZ.clicked.connect(self.MoveXYZ)
        self.btnXYZ.setVisible(False)
        layout.addWidget(self.btnXYZ, 1, 1)
        #
        self.btnX = QtGui.QPushButton("Move X")
        self.btnX.clicked.connect(self.MoveX)
        self.btnX.setVisible(False)
        layout.addWidget(self.btnX, 1, 0)
        #
        self.btnY = QtGui.QPushButton("Move Y")
        self.btnY.clicked.connect(self.MoveY)
        self.btnY.setVisible(False)
        layout.addWidget(self.btnY, 2, 0)
        #
        self.btnZ = QtGui.QPushButton("Move Z")
        self.btnZ.setVisible(False)
        self.btnZ.clicked.connect(self.MoveZ)
        layout.addWidget(self.btnZ, 3, 0)

    def CleanAll(self):
        FreeCAD.ActiveDocument.recompute()
        try:
            RemoveObservers()
        except:
            pass

    def reject(self):
        self.CleanAll()
        self.stack = []
        FreeCADGui.Control.closeDialog()

    def accept(self):
        self.CleanAll()
        self.stack = []
        FreeCADGui.Control.closeDialog()

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
        if str(sub).startswith("Vertex"):
            """Get names from  selected subelement and parent object"""
            docName = str(doc)
            objectName = str(obj)
            subElemetnName = str(sub)
            self.stack.append([objectName, subElemetnName,docName])


        if len(self.stack) == 1:
            self.lblPromt.setText("Select point on Second object!")
        if len(self.stack) == 2:
            """Update Gui"""
            self.lblPromt.setVisible(False)
            self.lblPromt.setText("Move object!")
            self.btnXYZ.setVisible(True)
            self.btnX.setVisible(True)
            self.btnY.setVisible(True)
            self.btnZ.setVisible(True)
            """Do Job"""
            self.GetSelectedObjects()

            """Clean all"""
            self.CleanAll()




    def GetSelectedObjects(self):
        FreeCAD.ActiveDocument.recompute()
        """Get first Object A"""
        self.objA = FreeCAD.getDocument(self.stack[0][2]).getObject(self.stack[0][0])
        print(self.stack[0][1])
        self.pointA = getObjectVertexFromName(self.objA, self.stack[0][1]).Point
        """Get second Object B"""
        self.objB = FreeCAD.getDocument(self.stack[1][2]).getObject(self.stack[1][0])
        self.pointB = getObjectVertexFromName(self.objB, self.stack[1][1]).Point

    def MoveXYZ(self):
        self.MoveSelections("xyz")

    def MoveX(self):
        pass
    def MoveY(self):
        pass
    def MoveZ(self):
        pass

    def MoveSelections(self, direction):
        FreeCAD.ActiveDocument.openTransaction("Move Object")
        Vector = self.pointB - self.pointA
        Pos0 = self.objA.Placement.Base
        Rot0 = self.objA.Placement.Rotation
        # Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation
        MVector = Pos0 + Vector
        self.objA.Placement = FreeCAD.Placement(MVector, Rot0)
        FreeCAD.ActiveDocument.commitTransaction()


def AlignPoints():
    global observer
    try:
        selGate = WBAuxiliaries.SelectionGate("Vertex")
        FreeCADGui.Selection.addSelectionGate(selGate)
        observer = SelObserverPointToPoint()
        FreeCADGui.Selection.addObserver(observer)
        FreeCADGui.Control.showDialog(observer)
    except:
        RemoveObservers()
        print(traceback.format_exc())


def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print("Observers are removed!")

AlignPoints()