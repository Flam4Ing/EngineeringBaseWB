import FreeCADGui

def cb(point):
            if point:
                print "got a 3D point: ",point
FreeCADGui.Snapper.getPoint(callback=cb)