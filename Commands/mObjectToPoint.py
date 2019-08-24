import FreeCAD
import FreeCADGui


def MoveToPoint():
    MouseSel = FreeCADGui.Selection.getSelectionEx()
    ObjA_Name = MouseSel[0].ObjectName
    PointObjB = MouseSel[1].SubObjects[0].Point
    ObjA = FreeCAD.ActiveDocument.getObject(ObjA_Name)
    ObjA.Placement.Base = PointObjB
    print(ObjA.Label + " is moved")


# MoveToPoint()

class SelectionGate(object):
    def __init__(self, to_select):
        self.toSelect = to_select

    def allow(self, doc, obj, sub):
        if not obj.isDerivedFrom("Part::Feature"):
            return False
        if str(sub).startswith(self.toSelect):
            return True
        return False


class SelObserverObjectToPoint:
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        print("Please select face on first object!")
        selGate = SelectionGate("Face")
        FreeCADGui.Selection.addSelectionGate(selGate)

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object

        if str(sub).startswith("Vertex") or str(sub).startswith("Face"):
            objPoint = FreeCAD.Vector(pnt[0], pnt[1], pnt[2])
            self.stack.append([str(obj), objPoint])
        if len(self.stack) == 1:
            print("Please select point on second object!")
            FreeCADGui.Selection.removeSelectionGate()
            selGate = SelectionGate("Vertex")
            FreeCADGui.Selection.addSelectionGate(selGate)
        if len(self.stack) == 2:
            ObjA_Name = self.stack[0][0]
            ObjB_Name = self.stack[1][0]
            PointA = self.stack[0][1]
            PointB = self.stack[1][1]
            # Vector = PointB - PointA
            # Pos0 = FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Base
            # Rot0 = FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Rotation
            # #Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation
            # MVector = Pos0 + Vector
            FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Base = PointB
            print("First object -" + ObjA_Name + "- is moved!")
            RemoveObservers()
            self.stack = []


# g = SelectionGate()
# FreeCADGui.Selection.addSelectionGate(g)
observer = SelObserverObjectToPoint()
FreeCADGui.Selection.addObserver(observer)


def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observer)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")
