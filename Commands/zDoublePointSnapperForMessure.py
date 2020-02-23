import FreeCADGui

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

s = DoublePointSnapper(1)
