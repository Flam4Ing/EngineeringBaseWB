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
        # self.toggle = 0
        self.GetSelTreeViewElement()


    def GetSelTreeViewElement(self):
        selTreeView = FreeCADGui.Selection.getSelectionEx()
        if len(selTreeView) > 0:
            self.selContainer = selTreeView[0].Object
            if (self.selContainer.isDerivedFrom('App::DocumentObjectGroup')):
                self.chkbMoveFolder.setText("Move selected folder <<" + self.selContainer.Label + ">> ?")
                self.isFolderSelected = True
            else:
                self.isFolderSelected = False

            if (self.selContainer.isDerivedFrom('App::Part')):
                self.chkbMoveFolder.setText("Move selected Part <<" + self.selContainer.Label + ">> ?")
                self.isPartSelected = True
            else:
                self.isPartSelected = False


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
        #
        self.chkbMoveFolder = QtGui.QCheckBox()
        self.chkbMoveFolder.setVisible(False)
        layout.addWidget(self.chkbMoveFolder, 4, 0)

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
            self.chkbMoveFolder.setVisible(True)


            """Do Job"""
            self.GetSelectedObjects()

            """Clean all"""
            self.CleanAll()




    def GetSelectedObjects(self):
        FreeCAD.ActiveDocument.recompute()
        """Get first Object A"""
        self.objA = FreeCAD.getDocument(self.stack[0][2]).getObject(self.stack[0][0])
        self.pointA = getObjectVertexFromName(self.objA, self.stack[0][1]).Point
        """Get second Object B"""
        self.objB = FreeCAD.getDocument(self.stack[1][2]).getObject(self.stack[1][0])
        self.pointB = getObjectVertexFromName(self.objB, self.stack[1][1]).Point
        """Get distance to move"""
        self.Vector = self.pointB - self.pointA


    def MoveXYZ(self):
        self.MoveSelections("xyz")

    def MoveX(self):
        self.MoveSelections("x")
    def MoveY(self):
        self.MoveSelections("y")
    def MoveZ(self):
        self.MoveSelections("z")


    def MoveSelections(self, direction):
        FreeCAD.ActiveDocument.openTransaction("Move Object")
        """Get Objects to move"""
        self.movedObjects = []
        if not (self.chkbMoveFolder.isChecked()):
            self.movedObjects.append(self.objA)

        if self.chkbMoveFolder.isChecked() and self.isFolderSelected:
            self.movedObjects = WBAuxiliaries.GetChildrenFromObject(self.selContainer)

        if self.chkbMoveFolder.isChecked() and self.isPartSelected:
            self.movedObjects.append(self.selContainer)

        """Move"""
        for obj in self.movedObjects:
            if hasattr(obj, "Placement"):
                Pos0 = obj.Placement.Base
                if direction == "xyz":
                    MVector = Pos0 + self.Vector
                if direction == "x":
                    Pos0.x = Pos0.x + self.Vector.x
                    MVector = Pos0
                if direction == "y":
                    Pos0.y = Pos0.y + self.Vector.y
                    MVector = Pos0
                if direction == "z":
                    Pos0.z = Pos0.z + self.Vector.z
                    MVector = Pos0
                obj.Placement.Base = MVector
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