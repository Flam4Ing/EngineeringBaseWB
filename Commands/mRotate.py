import Draft
import FreeCADGui

selection = FreeCADGui.Selection.getSelectionEx()
selObject = selection[0].Object

Draft.rotate(selObject, 15)