import FreeCAD
import FreeCADGui
import Part


class WiringDuct:
    def __init__(self, obj):
        obj.Proxy = self

    def execute(self, fp):
        V1 = FreeCAD.Vector(0, 0, 0)
        V2 = FreeCAD.Vector(0, fp.Width, 0)
        V3 = FreeCAD.Vector(0, fp.Width, fp.Height)
        V4 = FreeCAD.Vector(0, fp.Width-1, fp.Height)
        V5 = FreeCAD.Vector(0, fp.Width-1, 1 )
        V6 = FreeCAD.Vector(0, 1, 1)
        V7 = FreeCAD.Vector(0, 1, fp.Height)
        V8 = FreeCAD.Vector(0, 0, fp.Height)

        L1 = Part.LineSegment(V1, V2)
        L2 = Part.LineSegment(V2, V3)
        L3 = Part.LineSegment(V3, V4)
        L4 = Part.LineSegment(V4, V5)
        L5 = Part.LineSegment(V5, V6)
        L6 = Part.LineSegment(V6, V7)
        L7 = Part.LineSegment(V7, V8)
        L8 = Part.LineSegment(V8, V1)

        S1 = Part.Shape([L1, L2, L3, L4, L5, L6, L7, L8])
        W = Part.Wire(S1.Edges)
        F = Part.Face(W)
        railLength = fp.Length
        P = F.extrude(FreeCAD.Vector(railLength, 0, 0))
        obj1Part = FreeCAD.ActiveDocument.addObject("Part::Feature", "obj1Part")
        obj1Part.Shape = P
        #
        V51 = FreeCAD.Vector(12, 0, 10)
        V52 = FreeCAD.Vector(12, fp.Width, 10)
        V53 = FreeCAD.Vector(20, fp.Width, 10)
        V54 = FreeCAD.Vector(20, 0, 10)
        L51 = Part.LineSegment(V51, V52)
        L52 = Part.LineSegment(V52, V53)
        L53 = Part.LineSegment(V53, V54)
        L54 = Part.LineSegment(V54, V51)
        S50 = Part.Shape([L51, L52, L53, L54])
        W50 = Part.Wire(S50.Edges)
        F50 = Part.Face(W50)
        P50 = F50.extrude(FreeCAD.Vector(0, 0, fp.Height))
        obj2Part = FreeCAD.ActiveDocument.addObject("Part::Feature", "obj2Part")
        obj2Part.Shape = P50

        # import  Draft
        # cut = Draft.cut(obj1Part,obj2Part)

        # fp.Shape = Part.makeCompound([P,P50])
        # fp.Shape = cut.Shape
        import BOPTools.JoinFeatures
        j = BOPTools.JoinFeatures.makeCutout(name='Cutout')
        j.Base = obj1Part
        j.Tool = obj2Part
        j.Proxy.execute(j)
        j.purgeTouched()
        obj1Part.ViewObject.hide()
        obj2Part.ViewObject.hide()
        fp.Shape = j.Shape
        FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(j.Label)
        FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(obj1Part.Label)
        FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(obj2Part.Label)

class ViewProviderWiringDuct:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"



def GetWiringDuct(width = 60, height =40, length = 100):
    d = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "WiringDuct")
    d.addProperty("App::PropertyFloat", "Width", "Engineering Base Information", "Device width").Width = float(width)
    d.addProperty("App::PropertyFloat", "Height", "Engineering Base Information", "Device height").Height = float(height)
    d.addProperty("App::PropertyFloat", "Length", "Engineering Base Information", "Device length").Length = float(length)
    WiringDuct(d)
    ViewProviderWiringDuct(d.ViewObject)
    d.ViewObject.ShapeColor = (0.67, 0.67, 0.50)
    FreeCAD.ActiveDocument.recompute()
    return  d


if __name__ == "__main__":
    GetWiringDuct()