import FreeCAD
import FreeCADGui

def PlaceFacetoFace():
    '''1: select the first face (object master)
       2: select the second face (object to align)'''
    import Draft

    edgeO = FreeCADGui.Selection.getSelection()
    selectedFace = FreeCADGui.Selection.getSelectionEx()[0].SubObjects[0]  # select one element first face
    plDirection = FreeCAD.Placement(FreeCAD.Vector(0.0, 0.0, 0.0), FreeCAD.Rotation(0.0, 0.0, 0.0), FreeCAD.Vector(0.0, 0.0, 0.0))
    pointsTrajet = []

    yL = selectedFace.CenterOfMass  #
    uv = selectedFace.Surface.parameter(yL)
    nv = selectedFace.normalAt(uv[0], uv[1]).normalize().multiply(10.0)  # (length axis)
    pointsTrajet = [yL, (nv + yL)]
    direction = pointsTrajet[1].sub(pointsTrajet[0])
    r = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), direction)
    plDirection.Rotation.Q = r.Q

    pts = [yL, (nv + yL)]
    # lineAxis = Draft.makeWire([(yL - nv), (nv + yL)],closed=False,face=False,support=None) # create axis on face first object

    edgeO[1].Placement.Rotation = plDirection.Rotation  # second object with placement rotation first object

PlaceFacetoFace()