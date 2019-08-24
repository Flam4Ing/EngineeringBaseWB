import FreeCADGui
objToMove = FreeCADGui.Selection.getSelection()[0]
FreeCADGui.ActiveDocument.setEdit(objToMove,0)
