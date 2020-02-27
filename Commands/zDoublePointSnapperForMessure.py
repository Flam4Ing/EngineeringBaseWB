import FreeCADGui
import Draft
class DoublePointSnapper:
    #this gets a second point
    def __init__(self,val,point=None):
        self.pointStart = point
        self.val=val
        FreeCADGui.Snapper.getPoint(callback=self.clicked)
    def clicked(self,point,extra):
        # print (point)
        # print (self.val)
        if self.val==1:
            DoublePointSnapper(2, point)
        if self.val == 2:
            self.pointEnd = point
            # print(self.pointStart)
            # print (self.pointEnd)
            print(self.pointStart.sub(self.pointEnd))
            print (self.pointStart.sub(self.pointEnd).Length)
            dim = Draft.makeDimension(self.pointStart,self.pointEnd)
            dim.ViewObject.DisplayMode = "3D"
            dim.ViewObject.ArrowType = "Arrow"
            dim.ViewObject.ArrowSize = 10
s = DoublePointSnapper(1)
