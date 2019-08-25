
from PySide import QtGui, QtCore
from PySide.QtCore import *
from PySide.QtGui import *
import FreeCADGui
import WBAuxiliaries


class TransparencyControl(QtGui.QWidget):

    def __init__(self):
        super(TransparencyControl, self).__init__()      
        self.initUI()

    def initUI(self): 

        # create info label
        self.lbInfo = QtGui.QLabel('Transparency: ', self)
        self.lbInfo.move(10, 30)
        self.lbInfo.setFixedWidth(350)

        self.leEdit = QtGui.QLineEdit(self)
        self.leEdit.move(95, 26)
        
        self.btButton = QtGui.QPushButton('Do it!', self)
        self.btButton.clicked.connect(self.clickedButton)
        self.btButton.resize(self.btButton.minimumSizeHint())
        self.btButton.move(240, 26) 

        self.setGeometry(300, 350, 350, 80)
        self.setWindowTitle('Set Transparency')

    def clickedButton(self):
        selObjects = WBAuxiliaries.GetSelectionWithSubElements()
        if len(selObjects) != 0:
            transparencyValue = int(self.leEdit.text())
            for obj in selObjects:
                # if "Transparency" in dir(obj.ViewObject):
                if hasattr(obj.ViewObject, "Transparency"):
                    obj.ViewObject.Transparency = transparencyValue
        self.close()

    


vc = TransparencyControl()
vc.show()



