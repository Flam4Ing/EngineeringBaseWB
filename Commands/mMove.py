import FreeCADGui
try:
    objToMove = FreeCADGui.Selection.getSelection()[0]
    FreeCADGui.ActiveDocument.setEdit(objToMove,0)
except:
    print("The object is not selected!")