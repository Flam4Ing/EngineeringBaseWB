import FreeCAD
import FreeCADGui



sel = FreeCADGui.Selection.getSelectionEx()
if len(sel)>0:
    Obj_Name = sel[0].ObjectName

    Obj = FreeCAD.ActiveDocument.getObject(Obj_Name)
    print(Obj.Label)
    FreeCADGui.Selection.addSelection(Obj)
    # FreeCADGui.runCommand("Std_TreeSelection")
    FreeCADGui.runCommand('Std_TreeSelection', 0)