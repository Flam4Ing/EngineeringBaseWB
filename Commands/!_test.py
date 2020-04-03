import FreeCAD
import FreeCADGui
import WBAuxiliaries
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui
# import drafttaskpanels.task_circulararray
from drafttaskpanels.task_scale import *
# g = WBAuxiliaries.SelectionGate("Face")
# FreeCADGui.Selection.addSelectionGate(g)

# p = drafttaskpanels.task_circulararray.TaskPanelCircularArray()


class panelMy:
    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle("Move Part Object Point to Point")
        layout = QtGui.QGridLayout(self.form)
        self.InfoLabel = QtGui.QLabel("Info")
        layout.addWidget(self.InfoLabel, 0, 0)
        self.btnXYZ = QtGui.QPushButton("Move XYZ")
        self.btnXYZ.clicked.connect(self.MoveXYZ)
        layout.addWidget(self.btnXYZ, 1, 1)
        self.btnX = QtGui.QPushButton("Move X")
        self.btnX.clicked.connect(self.MoveXYZ)
        layout.addWidget(self.btnX, 1, 0)
        self.btnY = QtGui.QPushButton("Move Y")
        self.btnY.clicked.connect(self.MoveXYZ)
        layout.addWidget(self.btnY, 2, 0)
        self.btnZ = QtGui.QPushButton("Move Z")
        self.btnZ.clicked.connect(self.MoveXYZ)
        layout.addWidget(self.btnZ, 3, 0)
    def MoveXYZ(self):
        pass


p = panelMy()
Gui.Control.showDialog(p)