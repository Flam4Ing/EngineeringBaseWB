import FreeCAD
import FreeCADGui
import Part


class WiringDuct:
    def __init__(self, obj):
        obj.Proxy = self

    def execute(self, fp):
        self.wdWidth = fp.Width
        self.wdHeight = fp.Height
        self.wdLength = fp.Length


        import BOPTools.JoinFeatures
        j = BOPTools.JoinFeatures.makeCutout(name='Cutout')
        objBase = self.CreateBaseObject()
        objTool = self.CreateToolObject()
        j.Base = objBase
        j.Tool = objTool
        j.Proxy.execute(j)
        j.purgeTouched()
        objBase.ViewObject.hide()
        objTool.ViewObject.hide()
        fp.Shape = j.Shape
        FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(j.Label)
        FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(objBase.Label)
        # FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(objTool.Label)


    def CreateBaseObject(self):
        V1 = FreeCAD.Vector(0, 0, 0)
        V2 = FreeCAD.Vector(0, self.wdWidth, 0)
        V3 = FreeCAD.Vector(0, self.wdWidth, self.wdHeight)
        V4 = FreeCAD.Vector(0, self.wdWidth - 1, self.wdHeight)
        V5 = FreeCAD.Vector(0, self.wdWidth - 1, 1)
        V6 = FreeCAD.Vector(0, 1, 1)
        V7 = FreeCAD.Vector(0, 1, self.wdHeight)
        V8 = FreeCAD.Vector(0, 0, self.wdHeight)
        #
        L1 = Part.LineSegment(V1, V2)
        L2 = Part.LineSegment(V2, V3)
        L3 = Part.LineSegment(V3, V4)
        L4 = Part.LineSegment(V4, V5)
        L5 = Part.LineSegment(V5, V6)
        L6 = Part.LineSegment(V6, V7)
        L7 = Part.LineSegment(V7, V8)
        L8 = Part.LineSegment(V8, V1)
        #
        S1 = Part.Shape([L1, L2, L3, L4, L5, L6, L7, L8])
        W = Part.Wire(S1.Edges)
        F = Part.Face(W)
        P = F.extrude(FreeCAD.Vector(self.wdLength, 0, 0))
        objBase = FreeCAD.ActiveDocument.addObject("Part::Feature", "objBase")
        objBase.Shape = P
        return objBase

    def CreateToolObject(self):
        V1 = FreeCAD.Vector(12, 0, 10)
        V2 = FreeCAD.Vector(12, self.wdWidth-5, 10)
        V3 = FreeCAD.Vector(15, self.wdWidth, 10)
        V4 = FreeCAD.Vector(17, self.wdWidth, 10)
        V5 = FreeCAD.Vector(20, self.wdWidth-5, 10)
        V6 = FreeCAD.Vector(20, 0, 10)
        #
        L1 = Part.LineSegment(V1, V2)
        L2 = Part.LineSegment(V2, V3)
        L3 = Part.LineSegment(V3, V4)
        L4 = Part.LineSegment(V4, V5)
        L5 = Part.LineSegment(V5, V6)
        L6 = Part.LineSegment(V6, V1)
        #
        S = Part.Shape([L1, L2, L3, L4, L5, L6])
        W = Part.Wire(S.Edges)
        F = Part.Face(W)
        P = F.extrude(FreeCAD.Vector(0, 0, self.wdHeight))
        arrShape = []
        arrShape.append(P)
        qtyHoles = int(self.wdLength // 20)
        for i in range(1, qtyHoles):
            tc = P.copy()
            tc.Placement.Base = FreeCAD.Vector(tc.Placement.Base.x + 20 * i, 0, 0)
            arrShape.append(tc)

        objTool = FreeCAD.ActiveDocument.addObject("Part::Feature", "objTool")
        objTool.Shape = Part.makeCompound(arrShape)
        return objTool

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