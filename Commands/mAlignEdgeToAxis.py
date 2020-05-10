import FreeCAD
import FreeCADGui
from PySide import QtGui,QtCore
import WBAuxiliaries
from Utils.EB_Geometry import *
import Draft

def MoveEdgeToEdge():
    sel = FreeCAD.Gui.Selection.getSelectionEx()
    objA = sel[0].Object
    edgeA = sel[0].SubObjects[0]
    # edgeB = sel[1].SubObjects[0]
    # transform object A placement
    # edge vector
    edgeAEndPoint = edgeA.lastVertex(True).Point
    edgeAStartPoint = edgeA.firstVertex(True).Point
    # edgeBEndPoint = edgeB.lastVertex(True).Point
    # edgeBStartPoint = edgeB.firstVertex(True).Point

    va = (edgeAEndPoint - edgeAStartPoint).normalize()
    # vb = (edgeBEndPoint - edgeBStartPoint).normalize()
    vb = FreeCAD.Vector(1,0,0)
    # rot centre
    # centre = edgeAStartPoint
    centre = sel[0].SubObjects[1].Point
    # new placement
    print(FreeCAD.Rotation(va, vb).Angle)
    new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(va, vb), centre)
    # apply placement
    objA.Placement = new_plm.multiply(objA.Placement)
# MoveEdgeToEdge()

def reset_SelectedObjects(Selection, info=0):
    """ Reset the selection changed by Draft.rotate for example
    Selection is the original selection you want to reset. Must be saved before any
    change!
    """
    FreeCADGui.Selection.clearSelection()
    for Sel_i_Object in Selection:
        m_DocumentName = Sel_i_Object.DocumentName
        m_ObjectName = Sel_i_Object.ObjectName
        m_Object = Sel_i_Object.Object
        if info != 0:
            print_msg(str(m_Object))
        if len(Sel_i_Object.SubElementNames) == 0:
            if info != 0:
                print_msg(Sel_i_Object.ObjectName)
            FreeCADGui.Selection.addSelection(m_Object)
        else:
            for m_SubElementName in Sel_i_Object.SubElementNames:
                if info != 0:
                    m_finalName = str(m_DocumentName) + "." + str(m_ObjectName) + "." + str(m_SubElementName)
                    print_msg(m_finalName)
                FreeCADGui.Selection.addSelection(m_Object, str(m_SubElementName))





class EdgeParallelToAxis:
    def __init__(self):
        self.createGUI()
        self.GetSelTreeViewElement()

    def createGUI(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Align edge to axis")
        layout = QtGui.QGridLayout(self.form)
        #
        self.lblPromt = QtGui.QLabel()
        self.lblPromt.setText("Select edge and then a rotation point on the edge")
        layout.addWidget(self.lblPromt, 0, 0)
        #
        self.btnX = QtGui.QPushButton("Align to X-Axis")
        self.btnX.clicked.connect(self.AlignX)
        self.btnX.setVisible(True)
        layout.addWidget(self.btnX, 1, 0)
        #
        self.btnY = QtGui.QPushButton("Align to Y-Axis")
        self.btnY.clicked.connect(self.AlignY)
        self.btnY.setVisible(True)
        layout.addWidget(self.btnY, 2, 0)
        #
        self.btnZ = QtGui.QPushButton("Align to Z-Axis")
        self.btnZ.setVisible(True)
        self.btnZ.clicked.connect(self.AlignZ)
        layout.addWidget(self.btnZ, 3, 0)
        #
        self.chkbMoveFolder = QtGui.QCheckBox()
        self.chkbMoveFolder.setVisible(True)
        layout.addWidget(self.chkbMoveFolder, 4, 0)

    def reject(self):
        FreeCADGui.Control.closeDialog()

    def accept(self):
        FreeCADGui.Control.closeDialog()

    def GetSelection(self):
        self.selElememnts = FreeCAD.Gui.Selection.getSelectionEx()
        self.objA = self.selElememnts[0].Object
        edgeA = self.selElememnts[0].SubObjects[0]
        edgeAEndPoint = edgeA.lastVertex(True).Point
        edgeAStartPoint = edgeA.firstVertex(True).Point
        self.va = (edgeAEndPoint - edgeAStartPoint).normalize()
        self.centre = self.selElememnts[0].SubObjects[1].Point

        self.movedObjects = []
        if not (self.chkbMoveFolder.isChecked()):
            self.movedObjects.append(self.objA)

        if self.chkbMoveFolder.isChecked() and self.isFolderSelected:
            self.movedObjects = WBAuxiliaries.GetChildrenFromObject(self.selContainer)

        if self.chkbMoveFolder.isChecked() and self.isPartSelected:
            self.movedObjects.append(self.selContainer)



    def GetSelTreeViewElement(self):
        selTreeView = FreeCADGui.Selection.getSelectionEx()
        if len(selTreeView) > 0:
            self.selContainer = selTreeView[0].Object
            if (self.selContainer.isDerivedFrom('App::DocumentObjectGroup')):
                self.chkbMoveFolder.setVisible(True)
                self.chkbMoveFolder.setText("Move selected folder <<" + self.selContainer.Label + ">> ?")
                self.isFolderSelected = True
            else:
                self.isFolderSelected = False

            if (self.selContainer.isDerivedFrom('App::Part')):
                self.chkbMoveFolder.setVisible(True)
                self.chkbMoveFolder.setText("Move selected Part <<" + self.selContainer.Label + ">> ?")
                self.isPartSelected = True
            else:
                self.isPartSelected = False


    def AlignX(self):
        self.MoveSelections("x")
    def AlignY(self):
        self.MoveSelections("y")
    def AlignZ(self):
        self.MoveSelections("z")

    def MoveSelections(self, direction):
        self.GetSelection()
        FreeCAD.ActiveDocument.openTransaction("Move Object")
        if direction == "x":
            vb = FreeCAD.Vector(1,0,0)
            m_angle, m_angle_rad = angleBetween(self.va, vb)
            if m_angle == 0:
                vb = FreeCAD.Vector(-1, 0, 0)

        if direction == "y":
            vb = FreeCAD.Vector(0,1,0)
            m_angle, m_angle_rad = angleBetween(self.va, vb)
            if m_angle == 0:
                vb = FreeCAD.Vector(0, -1, 0)

        if direction == "z":
            vb = FreeCAD.Vector(0,0,1)
            m_angle, m_angle_rad = angleBetween(self.va, vb)
            if m_angle == 0:
                vb = FreeCAD.Vector(0, 0, -1)

            # m_angle, m_angle_rad = angleBetween(self.va, vb)
            # if m_angle == 0:
            #     rot_angle = 180.
            # else:
            #     rot_angle = m_angle
            # rot_axis = self.va.cross(vb)
            # rot_center = self.centre
            # Draft.rotate(self.objA, rot_angle, rot_center, rot_axis)
            # reset_SelectedObjects(self.selElememnts, info=0)



        new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(self.va, vb), self.centre)
        for obj in self.movedObjects:
            obj.Placement = new_plm.multiply(obj.Placement)
        FreeCAD.ActiveDocument.commitTransaction()


def AlignToAxis():
    edgeParallel = EdgeParallelToAxis()
    FreeCADGui.Control.showDialog(edgeParallel)

AlignToAxis()