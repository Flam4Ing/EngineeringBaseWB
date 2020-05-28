import  FreeCAD


def GetSelFace():
    sel = FreeCAD.Gui.Selection.getSelectionEx()
    Face = sel[0].SubObjects[0]
    print(Face.Area)



import Utils.EB_Geometry
# glb = (1.0, 1.0, 0.0)  # yellow
# # grn = (0.,1.,0.) #green
# sel = FreeCAD.Gui.Selection.getSelectionEx()
# obj = sel[0].Object
# Utils.EB_Geometry.SetFaceColour(obj, glb, [2500, 499])
GetSelFace()
