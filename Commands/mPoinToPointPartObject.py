import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
global selObject
global observer

class SelObserverPointToPoint:
    def __init__(self, movedObjects):
        self.createGUI()
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        self.movedObjects = movedObjects


    def createGUI(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Move Part Object Point to Point")
        layout = QtGui.QGridLayout(self.form)
        #
        self.InfoLabel = QtGui.QLabel()
        self.InfoLabel.setText("Select point on First object!")
        layout.addWidget(self.InfoLabel, 0, 0)
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
            self.Vector = PointB - PointA

            # Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation

            # FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement = FreeCAD.Placement(MVector, Rot0)
            self.InfoLabel.setText("Move object!")
            self.btnXYZ.setVisible(True)
            self.btnX.setVisible(True)
            self.btnY.setVisible(True)
            self.btnZ.setVisible(True)


    def MoveSelections(self, direction):
        FreeCAD.ActiveDocument.openTransaction("Move Object")

        for obj in self.movedObjects:
            print(obj.Name)
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
        RemoveObservers()
        self.stack = []
        FreeCADGui.Control.closeDialog()

    def MoveXYZ(self):
        self.MoveSelections("xyz")
    def MoveX(self):
        self.MoveSelections("x")
    def MoveY(self):
        self.MoveSelections("y")
    def MoveZ(self):
        self.MoveSelections("z")

def MoveObject():
    try:

        global selObject
        movedObjects = []
        selection = FreeCADGui.Selection.getSelectionEx()
        selObject = selection[0].Object

        if len(selection) != 1:
            WBAuxiliaries.MsgDialog("Please first select one Part Object!")
            return
        if not (selObject.isDerivedFrom('App::DocumentObjectGroup') or selObject.isDerivedFrom('App::Part')):
            WBAuxiliaries.MsgDialog("Please first select one Part Object!")
            return

        def StartObserver(movedObjects):
            global observer
            selGate = WBAuxiliaries.SelectionGate("Vertex")
            FreeCADGui.Selection.addSelectionGate(selGate)
            observer = SelObserverPointToPoint(movedObjects)
            FreeCADGui.Selection.addObserver(observer)
            print(selObject.Name + " - is selected!")
            FreeCADGui.Control.showDialog(observer)

        if selObject.isDerivedFrom('App::Part'):
            movedObjects.append(selection[0].Object)
            StartObserver(movedObjects)

        if selObject.isDerivedFrom('App::DocumentObjectGroup'):
            movedObjects = WBAuxiliaries.GetSelectionWithSubElements()
            StartObserver(movedObjects)

        FreeCADGui.Selection.clearSelection()

    except:
        FreeCADGui.Selection.removeObserver(observer)
        FreeCADGui.Selection.removeSelectionGate()
        print("Observers are removed!")

def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")

MoveObject()