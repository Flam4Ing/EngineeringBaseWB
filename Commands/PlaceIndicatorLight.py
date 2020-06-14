import FreeCAD
import FreeCADGui
import EB_D_DoorControls
import EB_Auxiliaries

def clicked(point):
    FreeCAD.ActiveDocument.openTransaction("Place indicator light")
    sh = EB_D_DoorControls.GetIndicatorLight()
    sh.Placement.Base = point
    FreeCAD.ActiveDocument.commitTransaction()
FreeCADGui.Snapper.getPoint(callback=clicked)