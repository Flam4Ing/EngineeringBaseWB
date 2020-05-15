import FreeCADGui
import clsShapeFromSTEP
import EB_Auxiliaries



def clicked(point):
    sh = clsShapeFromSTEP.GetShapeFromSTEP("Cable Gland", EB_Auxiliaries.CableGlandsPath())
    sh.ViewObject.ShapeColor = (0.67,0.67,0.50)
    sh.Placement.Base = point
FreeCADGui.Snapper.getPoint(callback=clicked)






