import FreeCAD
import FreeCADGui


class SelObserver:
    def setPreselection(self, doc, obj, sub):  # Preselection object
        FreeCAD.Console.PrintMessage(str(sub) + "\n")  # The part of the object name

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        FreeCAD.Console.PrintMessage("addSelection" + "\n")
        FreeCAD.Console.PrintMessage(str(doc) + "\n")  # Name of the document
        FreeCAD.Console.PrintMessage(str(obj) + "\n")  # Name of the object
        FreeCAD.Console.PrintMessage(str(sub) + "\n")  # The part of the object name
        FreeCAD.Console.PrintMessage(str(pnt) + "\n")  # Coordinates of the object
        FreeCAD.Console.PrintMessage("______" + "\n")

    def removeSelection(self, doc, obj, sub):  # Delete the selected object
        FreeCAD.Console.PrintMessage("removeSelection" + "\n")

    def setSelection(self, doc):  # Selection in ComboView
        FreeCAD.Console.PrintMessage("setSelection" + "\n")

    def clearSelection(self, doc):  # If click on the screen, clear the selection
        FreeCAD.Console.PrintMessage("clearSelection" + "\n")  # If click on another object, clear the previous object


s = SelObserver()
FreeCADGui.Selection.addObserver(s)
# FreeCADGui.Selection.removeObserver(s)
