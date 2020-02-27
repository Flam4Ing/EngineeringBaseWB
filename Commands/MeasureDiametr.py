import FreeCAD
import FreeCADGui
import Draft
import Part

sel = FreeCADGui.Selection.getSelectionEx()
if len(sel)==1:

    if "Edge" in sel[0].SubElementNames[0]:
        edge = sel[0].SubObjects[0]
        if isinstance(edge.Curve, Part.Circle):
            print(edge.Curve.Radius)