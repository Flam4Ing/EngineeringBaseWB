import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import EB_Auxiliaries
from Utils.EB_Geometry import *
import Draft
import Part
global observer


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
        #
        self.lblPromt = QtGui.QLabel()
        self.lblPromt.setText("Select edge on First object!")
        layout.addWidget(self.lblPromt, 0, 0)
        #
        self.btnRotate = QtGui.QPushButton("Flip")
        self.btnRotate.clicked.connect(self.Flip)
        self.btnRotate.setVisible(False)
        layout.addWidget(self.btnRotate, 1, 1)
        #
        self.btnJointEdges = QtGui.QPushButton("Joint Edges")
        self.btnJointEdges.clicked.connect(self.JointEdges)
        self.btnJointEdges.setVisible(False)
        layout.addWidget(self.btnJointEdges, 2, 1)
        #
        self.lblInfo = QtGui.QLabel()
        self.lblInfo.setText("Select two faces to align!")
        self.lblInfo.setVisible(False)
        layout.addWidget(self.lblInfo, 3, 1)
        #
        self.btnAlignFaces = QtGui.QPushButton("Align Faces")
        self.btnAlignFaces.clicked.connect(self.AlignFaces)
        self.btnAlignFaces.setVisible(False)
        layout.addWidget(self.btnAlignFaces, 4, 1)


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
            docName = str(doc)
            objectName = str(obj)
            subElemetnName = str(sub)
            self.stack.append([objectName, subElemetnName, docName])

            """Get selected object with subelement"""
            # sel = FreeCAD.Gui.Selection.getSelectionEx()
            # mainObj = sel[0].Object
            # subObj = sel[0].SubObjects[0]
            # self.stack.append([mainObj, subObj])
        if len(self.stack) == 1:
            self.lblPromt.setText("Select edge on Second object")
        if len(self.stack) == 2:
            """Update Gui"""
            self.lblPromt.setVisible(False)
            self.btnRotate.setVisible(True)
            self.btnJointEdges.setVisible(True)
            self.btnAlignFaces.setVisible(True)
            self.lblInfo.setVisible(True)

            """Do Job"""
            self.GetSelectedObjects()
            # self.Flip()
            #self.Move()

            """Clean all"""
            self.CleanAll()

    def GetSelectedObjects(self):
        FreeCAD.ActiveDocument.recompute()
        """Get first Object A"""
        self.objA = FreeCAD.getDocument(self.stack[0][2]).getObject(self.stack[0][0])
        self.edgeA = getObjectEdgeFromName(self.objA, self.stack[0][1])
        self.edgeA_EndPoint = self.edgeA.lastVertex(True).Point
        self.edgeA_StartPoint = self.edgeA.firstVertex(True).Point
        self.edgeA_MidPoint = (self.edgeA_EndPoint + self.edgeA_StartPoint).multiply(0.5)

        """Get second Object B"""
        self.objB = FreeCAD.getDocument(self.stack[1][2]).getObject(self.stack[1][0])
        self.edgeB = getObjectEdgeFromName(self.objB, self.stack[1][1])
        self.edgeB_EndPoint = self.edgeB.lastVertex(True).Point
        self.edgeB_StartPoint = self.edgeB.firstVertex(True).Point
        self.edgeB_MidPoint = (self.edgeB_EndPoint + self.edgeB_StartPoint).multiply(0.5)
        self.va = (self.edgeA_EndPoint - self.edgeA_StartPoint).normalize()
        self.vb = (self.edgeB_EndPoint - self.edgeB_StartPoint).normalize()



    def Flip(self):
        FreeCAD.ActiveDocument.openTransaction("Align edge - rotate")
        self.GetSelectedObjects()
        self.Rotate()
        FreeCAD.ActiveDocument.commitTransaction()


    def Rotate(self):
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



    def RotFromDraft(self):
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


    def JointEdges(self):
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

    def AlignFaces(self):
        self.GetSelectedObjects()

        sel = FreeCAD.Gui.Selection.getSelectionEx()
        if len(sel) == 2:
            if isinstance(sel[0].SubObjects[0], Part.Face) and isinstance(sel[1].SubObjects[0], Part.Face):
                rot_center = self.edgeA_MidPoint
                rot_axis = edgeToVector(self.edgeA)
                selFace1Normal = sel[0].SubObjects[0].normalAt(0, 0)
                selFace2Normal = sel[1].SubObjects[0].normalAt(0, 0)
                m_angle, m_angle_rad = angleBetween(selFace1Normal, selFace2Normal)
                if m_angle < 180:
                    diff_angle = 180 - m_angle
                    # print("Kleiner 180 - " + str(m_angle))
                elif m_angle > 180:
                    diff_angle = 360 - m_angle
                    # print("Grosser 180 - " + str(m_angle))
                elif m_angle == 180:
                    diff_angle = -180
                    # print("Gleich 180 - " + str(m_angle))
                rot = FreeCAD.Rotation(rot_axis, diff_angle)
                self.objA.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), rot, rot_center).multiply(self.objA.Placement)


def AlignEdges():
    global observer
    try:
        selGate = EB_Auxiliaries.SelectionGate("Edge")
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