import FreeCAD
import FreeCADGui
import WBAuxiliaries


g = WBAuxiliaries.SelectionGate("Face")
FreeCADGui.Selection.addSelectionGate(g)

