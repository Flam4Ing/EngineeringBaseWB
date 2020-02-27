import FreeCAD
import FreeCADGui
import Draft

sel = FreeCADGui.Selection.getSelectionEx()
if len(sel)==1:
    ObjA_Name = sel[0].ObjectName
    # print(ObjA_Name)
    # print(sel[0].Object.Name)
    ObjA = FreeCAD.ActiveDocument.getObject(ObjA_Name)
    if "Edge" in sel[0].SubElementNames[0]:
        edge = sel[0].SubObjects[0]
        print(edge.Curve.Radius)
        n = int(sel[0].SubElementNames[0].lstrip("Edge"))-1
        # print(sel[0].SubElementNames[0])
        dim = Draft.makeDimension(sel[0].Object, n, "diameter")
        dim.ViewObject.DisplayMode = "3D"
        dim.ViewObject.ArrowType = "Arrow"
        FreeCAD.ActiveDocument.recompute()
        # dim.ViewObject.ArrowSize = 10