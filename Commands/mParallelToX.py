import FreeCAD
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
MoveEdgeToEdge()