import FreeCAD
import FreeCADGui
import EB_D_DoorControls
import EB_Auxiliaries

def clicked(point):
    FreeCAD.ActiveDocument.openTransaction("Place indicator light")
    sh = EB_D_DoorControls.GetDoorSwitches()
    sh.Placement.Base = point
    sh.FrontPartColour = "Yellow"
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.commitTransaction()
FreeCADGui.Snapper.getPoint(callback=clicked)