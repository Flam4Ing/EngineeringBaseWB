import FreeCAD
import FreeCADGui
import WBAuxiliaries

#Beispiel
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
#End Beispiel


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
            FreeCAD.ActiveDocument.openTransaction("Align edges")
            objA = self.stack[0][0]
            edgeA = self.stack[0][1]
            edgeB = self.stack[1][1]
            # transform object A placement
            # edge vector
            edgeA_EndPoint = edgeA.lastVertex(True).Point
            edgeA_StartPoint = edgeA.firstVertex(True).Point
            edgeA_MidPoint = (edgeA_EndPoint + edgeA_StartPoint).multiply(0.5)
            edgeB_EndPoint = edgeB.lastVertex(True).Point
            edgeB_StartPoint = edgeB.firstVertex(True).Point
            edgeB_MidPoint = (edgeB_EndPoint + edgeB_StartPoint).multiply(0.5)
            va = (edgeA_EndPoint - edgeA_StartPoint).normalize()
            vb = (edgeB_EndPoint - edgeB_StartPoint).normalize()
            angleToRotate = FreeCAD.Rotation(va, vb)

            # rot centre
            #center = edgeA_StartPoint
            center = edgeA_MidPoint
            # new placement
            new_plm = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), angleToRotate, center)
            # apply placement
            objA.Placement = new_plm.multiply(objA.Placement)
            # laying on edge
            #distatceVector = edgeA_StartPoint - edgeB_StartPoint
            distatceVector = edgeA_MidPoint - edgeB_MidPoint
            MVector = objA.Placement.Base - distatceVector
            objA.Placement.Base = MVector
            FreeCAD.ActiveDocument.commitTransaction()

            print("First object -" + str(objA.Label) + "- is moved!")
            RemoveObservers()
            self.stack = []


selGate = WBAuxiliaries.SelectionGate("Edge")
FreeCADGui.Selection.addSelectionGate(selGate)
observerEtE = SelObserverEdgeToEdge()
FreeCADGui.Selection.addObserver(observerEtE)


def RemoveObservers():
    FreeCADGui.Selection.removeObserver(observerEtE)
    FreeCADGui.Selection.removeSelectionGate()
    print ("Observers are removed!")
