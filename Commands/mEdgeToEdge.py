import FreeCAD
import FreeCADGui


def MoveEdgeToEdge():
    sel = FreeCAD.Gui.Selection.getSelectionEx()
    objA = sel[0].Object
    edgeA = sel[0].SubObjects[0]
    edgeB = sel[1].SubObjects[0]
    # transform object A placement
    # edge vector
    edgeAEndPoint = edgeA.lastVertex(True).Point
    edgeAStartPoint = edgeA.firstVertex(True).Point
    edgeBEndPoint = edgeB.lastVertex(True).Point
    edgeBStartPoint = edgeB.firstVertex(True).Point

    va = (edgeAEndPoint - edgeAStartPoint).normalize()
    vb = (edgeBEndPoint - edgeBStartPoint).normalize()
    # rot centre
    centre = edgeAStartPoint
    # new placement
    new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(va, vb), centre)
    # apply placement
    objA.Placement = new_plm.multiply(objA.Placement)


# MoveEdgeToEdge()


class SelectionGate(object):
    def allow(self, doc, obj, sub):
        if not obj.isDerivedFrom("Part::Feature"):
            return False
        if str(sub).startswith("Edge"):
            return True
        return False


class SelObserverEdgeToEdge:
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        print("Please select edge on first object!")

    def addSelection(self, doc, obj, sub, pnt):  # Selection object
        # FreeCAD.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        # FreeCAD.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        # FreeCAD.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        # FreeCAD.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object

        if str(sub).startswith("Edge"):
            sel = FreeCAD.Gui.Selection.getSelectionEx()
            mainObj = sel[0].Object
            subObj = sel[0].SubObjects[0]
            self.stack.append([mainObj, subObj])
        if len(self.stack) == 1:
            print("Please select edge on second object!")
        if len(self.stack) == 2:
            objA = self.stack[0][0]
            edgeA = self.stack[0][1]
            edgeB = self.stack[1][1]
            # transform object A placement
            # edge vector
            edgeAEndPoint = edgeA.lastVertex(True).Point
            edgeAStartPoint = edgeA.firstVertex(True).Point
            edgeBEndPoint = edgeB.lastVertex(True).Point
            edgeBStartPoint = edgeB.firstVertex(True).Point
            va = (edgeAEndPoint - edgeAStartPoint).normalize()
            vb = (edgeBEndPoint - edgeBStartPoint).normalize()
            # rot centre
            centre = edgeAStartPoint
            # new placement
            new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), FreeCAD.Rotation(va, vb), centre)
            # apply placement
            objA.Placement = new_plm.multiply(objA.Placement)
            # laying on edge
            Vector = edgeA.firstVertex(True).Point - edgeB.firstVertex(True).Point
            MVector = objA.Placement.Base - Vector
            objA.Placement.Base = MVector

            print("First object -" + str(objA.Label) + "- is moved!")
            RemoveObservers()
            self.stack = []


g = SelectionGate()
FreeCADGui.Selection.addSelectionGate(g)
observerEtE = SelObserverEdgeToEdge()
FreeCADGui.Selection.addObserver(observerEtE)


def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observerEtE)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")
