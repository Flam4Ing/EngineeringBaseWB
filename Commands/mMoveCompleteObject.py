import FreeCAD
import FreeCADGui

import WBAuxiliaries
global selObject

class SelObserverPointToPoint:
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        print("Please select point on first object!")

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
            print("Please select point on second object!")
        if len(self.stack) == 2:
            ObjA_Name = self.stack[0][0]
            ObjB_Name = self.stack[1][0]
            PointA = self.stack[0][1]
            PointB = self.stack[1][1]
            Vector = PointB - PointA
            Pos0 = selObject.Placement.Base
            Rot0 = selObject.Placement.Rotation
            # Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation
            MVector = Pos0 + Vector
            # FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement = FreeCAD.Placement(MVector, Rot0)
            selObject.Placement.Base = MVector
            print("First object -" + selObject.Name + "- is moved!")
            RemoveObservers()
            self.stack = []

try:
    selection = FreeCADGui.Selection.getSelectionEx()
    if len(selection) == 1:
        selObject = selection[0].Object
        selGate = WBAuxiliaries.SelectionGate("Vertex")
        FreeCADGui.Selection.addSelectionGate(selGate)
        observer = SelObserverPointToPoint()
        FreeCADGui.Selection.addObserver(observer)
        print(selObject.Name + " - is selected!")
    else:
        print("Please first select one object!")

except:
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print("Observers are removed!")

def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")
