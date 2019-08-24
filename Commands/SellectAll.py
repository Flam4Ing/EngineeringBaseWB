import FreeCAD
for obj in FreeCAD.ActiveDocument.Objects:
    objName = obj.Name
    obj = App.ActiveDocument.getObject(objName)
    Gui.Selection.addSelection(obj)
