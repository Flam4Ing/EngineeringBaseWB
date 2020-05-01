import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
from Utils.EB_Geometry import *
import Draft
global observer

def find(anEdge,inObject):
    for e in inObject.Shape.Edges:
        if e.Vertexes[0].Point == anEdge.Vertexes[0].Point:
               if e.Vertexes[-1].Point == anEdge.Vertexes[-1].Point:
                   return inObject.Shape.Edges.index(e) # we return the index of the edge in the edges list
    return None



class SelObserverEdgeToEdge:
    def __init__(self):
        self.createGUI()
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        self.toggle = 0

    def createGUI(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Align Edges")
        layout = QtGui.QGridLayout(self.form)
        self.InfoLabel = QtGui.QLabel()
        self.InfoLabel.setText("Select edge on First object!")
        layout.addWidget(self.InfoLabel, 0, 0)
        self.btnRotate = QtGui.QPushButton("Flip")
        self.btnRotate.clicked.connect(self.Flip)
        layout.addWidget(self.btnRotate, 1, 1)
        self.btnMoveToggle = QtGui.QPushButton("Move")
        self.btnMoveToggle.clicked.connect(self.MoveToggle)
        layout.addWidget(self.btnMoveToggle, 2, 1)
        self.btnMoveStart = QtGui.QPushButton("Spare")
        self.btnMoveStart.clicked.connect(self.Spare)
        layout.addWidget(self.btnMoveStart, 3, 1)



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

        if str(sub).startswith("Edge"):
            """Get names from  selected subelement and parent object"""
            self.docName = str(doc)
            objectName = str(obj)
            edgeNumber = int(str(sub)[4:])
            self.stack.append([objectName, edgeNumber])

            """Get selected object with subelement"""
            # sel = FreeCAD.Gui.Selection.getSelectionEx()
            # mainObj = sel[0].Object
            # subObj = sel[0].SubObjects[0]
            # self.stack.append([mainObj, subObj])
        if len(self.stack) == 1:
            self.InfoLabel.setText("Select edge on Second object")
        if len(self.stack) == 2:
            self.InfoLabel.setVisible(False)
            self.GetSelectedObjects()
            self.Flip()
            #self.Move()

            """Clean all"""
            self.CleanAll()



    def GetSelectedObjects(self):
        FreeCAD.ActiveDocument.recompute()
        """Get first Object A"""
        self.objA = FreeCAD.getDocument(self.docName).getObject(self.stack[0][0])
        edgeA_Number = self.stack[0][1] - 1
        self.edgeA = self.objA.Shape.Edges[edgeA_Number]
        self.edgeA_EndPoint = self.edgeA.lastVertex(True).Point
        self.edgeA_StartPoint = self.edgeA.firstVertex(True).Point
        self.edgeA_MidPoint = (self.edgeA_EndPoint + self.edgeA_StartPoint).multiply(0.5)
        # print(self.objA.Name)
        # print("EdgeA-" + str(edgeA_Number) + " Length-" + str(self.edgeA.Length) +"mm")

        """Get second Object B"""
        self.objB = FreeCAD.getDocument(self.docName).getObject(self.stack[1][0])
        edgeB_Number = self.stack[1][1] - 1
        self.edgeB = self.objB.Shape.Edges[edgeB_Number]
        self.edgeB_EndPoint = self.edgeB.lastVertex(True).Point
        self.edgeB_StartPoint = self.edgeB.firstVertex(True).Point
        self.edgeB_MidPoint = (self.edgeB_EndPoint + self.edgeB_StartPoint).multiply(0.5)
        self.va = (self.edgeA_EndPoint - self.edgeA_StartPoint).normalize()
        self.vb = (self.edgeB_EndPoint - self.edgeB_StartPoint).normalize()
        # print(self.objB.Name)
        # print("EdgeB-" + str(edgeB_Number) + " Length-" + str(self.edgeB.Length) +"mm")

    def Flip(self):
        FreeCAD.ActiveDocument.openTransaction("Align edge - rotate")
        self.GetSelectedObjects()
        self.Rot1()
        FreeCAD.ActiveDocument.commitTransaction()


    def Rot1(self):
        if colinearEdges(self.edgeA, self.edgeB):
            # print(angleBetween(self.edgeA, self.edgeB))
            rot_axis = FreeCAD.Base.Vector(0, 0, 1).cross(edgeToVector(self.edgeA))
            self.angleToRotate = FreeCAD.Rotation(rot_axis, 180)
        else:
            self.angleToRotate = FreeCAD.Rotation(self.va, self.vb)
        self.center = self.edgeA_MidPoint

        """new placement"""
        new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), self.angleToRotate, self.center)
        self.objA.Placement = new_plm.multiply(self.objA.Placement)


    def Rot2(self):
        if colinearEdges(self.edgeA, self.edgeB):
            rot_axis = FreeCAD.Base.Vector(0, 0, 1).cross(edgeToVector(self.edgeA))
            rot_center = self.edgeA_MidPoint
            rot_angle = 180.
            Draft.rotate(self.objA, rot_angle, rot_center, rot_axis)
        else:
            m_angle, m_angle_rad = angleBetween(self.edgeA, self.edgeB)
            rot_axis = edgeToVector(self.edgeA).cross(edgeToVector(self.edgeB))
            rot_center = self.edgeA_MidPoint
            rot_angle = m_angle
            Draft.rotate(self.objA, rot_angle, rot_center, rot_axis)


    def MoveToggle(self):
        self.GetSelectedObjects()
        self.toggle = self.toggle +1
        if (self.toggle == 1):
            distatceVector = self.edgeA_MidPoint - self.edgeB_MidPoint
        if (self.toggle == 2):
            distatceVector = self.edgeA_StartPoint - self.edgeB_StartPoint
        if (self.toggle == 3):
            distatceVector = self.edgeA_EndPoint - self.edgeB_EndPoint
            self.toggle = 0

        """laying edges on middle point"""
        FreeCAD.ActiveDocument.openTransaction("Align edge - move")

        MVector = self.objA.Placement.Base - distatceVector
        self.objA.Placement.Base = MVector
        FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()

    def Spare(self):
        self.GetSelectedObjects()
        rot_center = self.edgeA_MidPoint
        rot_axis = edgeToVector(self.edgeA)
        rot = FreeCAD.Rotation(rot_axis, 15)
        self.objA.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), rot, rot_center).multiply(self.objA.Placement)
        sel = FreeCAD.Gui.Selection.getSelectionEx()
        selFace1 = sel[0].SubObjects[0].normalAt(0, 0)
        selFace2 = sel[1].SubObjects[0].normalAt(0, 0)
        print (angleBetween(selFace1, selFace2))



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