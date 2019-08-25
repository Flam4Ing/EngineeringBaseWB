import FreeCADGui
import clsShapeFromSTEP
import WBAuxiliaries



def clicked(point):
    sh = clsShapeFromSTEP.GetShapeFromSTEP("Cable Gland", WBAuxiliaries.CableGlandsPath())
    sh.ViewObject.ShapeColor = (0.67,0.67,0.50)
    sh.Placement.Base = point
FreeCADGui.Snapper.getPoint(callback=clicked)






