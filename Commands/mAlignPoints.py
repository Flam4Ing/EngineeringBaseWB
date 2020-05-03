import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
import  traceback

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

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
        if str(sub).startswith("Vertex"):
            """Get names from  selected subelement and parent object"""
            self.docName = str(doc)
            objectName = str(obj)
            edgeNumber = int(str(sub)[6:])
            self.stack.append([objectName, edgeNumber])
            print(edgeNumber)


        if len(self.stack) == 1:
            self.lblPromt.setText("Select point on Second object!")
        if len(self.stack) == 2:
            self.lblPromt.setVisible(False)
            self.lblPromt.setText("Move object!")
            self.btnXYZ.setVisible(True)
            self.btnX.setVisible(True)
            self.btnY.setVisible(True)
            self.btnZ.setVisible(True)

            """Clean all"""
            self.CleanAll()


    def accept(self):
        self.CleanAll()
        self.stack = []
        FreeCADGui.Control.closeDialog()

    def MoveXYZ(self):
        pass

    def MoveX(self):
        pass
    def MoveY(self):
        pass
    def MoveZ(self):
        pass


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