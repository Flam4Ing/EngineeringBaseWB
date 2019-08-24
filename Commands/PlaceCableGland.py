import clsShapeFromSTEP
import WBAuxiliaries



def clicked(point):
    sh = clsShapeFromSTEP.GetShapeFromSTEP("Cable Gland", WBAuxiliaries.CableGlandsPath())
    sh.ViewObject.ShapeColor = (0.67,0.67,0.50)
    sh.Placement.Base = point
FreeCADGui.Snapper.getPoint(callback=clicked)

class DoublePointSnapper:
    #this gets a second point
    def __init__(self,val):
        self.point = None
        self.val=val
        FreeCADGui.Snapper.getPoint(callback=self.clicked)
    def clicked(self,point,extra):
        self.point = point
        print point
        print self.val
        if self.val==1:
            DoublePointSnapper(2)
#s = DoublePointSnapper(1)