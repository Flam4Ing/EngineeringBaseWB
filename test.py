import  FreeCAD


def GetSelFace():
    sel = FreeCAD.Gui.Selection.getSelectionEx()
    Face = sel[0].SubObjects[0]
    print(Face.Area)

def SetFaceColour(obj, colour, facesBYareas, tolerance=1):
    numfaces = len(obj.Shape.Faces)
    """1 = 255
    color numer 10 = (1/255) * 10
    color numer 75 = (1/255) * 75"""


    # colors = [rgb for i in range(numfaces)]
    defaultColour = obj.ViewObject.DiffuseColor[0]
    colors = []
    for i in obj.Shape.Faces:
        col = defaultColour
        for f in facesBYareas:
            if i.Area > f - tolerance and i.Area < f + tolerance:
                col = colour
                break

        colors.append(col)

    obj.ViewObject.DiffuseColor = colors


glb = (1.0, 1.0, 0.0)  # yellow
# grn = (0.,1.,0.) #green
sel = FreeCAD.Gui.Selection.getSelectionEx()
obj = sel[0].Object
# print(obj.ViewObject.DiffuseColor[0])
SetFaceColour(obj, glb, [2500, 499])

GetSelFace()
