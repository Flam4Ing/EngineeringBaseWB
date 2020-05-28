import EB_Auxiliaries
import FreeCAD
import FreeCADGui
import Part


class DINRailTS35:
    def __init__(self, obj):
        obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        if fp.Height == "7.5":
            V1 = FreeCAD.Vector(0, 35, 6.5)
            V2 = FreeCAD.Vector(0, 31, 6.5)
            V5 = FreeCAD.Vector(0, 4, 6.5)
            V6 = FreeCAD.Vector(0, 0, 6.5)
            V7 = FreeCAD.Vector(0, 0, 7.5)
            V8 = FreeCAD.Vector(0, 5, 7.5)
            V11 = FreeCAD.Vector(0, 30, 7.5)
            V12 = FreeCAD.Vector(0, 35, 7.5)
        else:
            V1 = FreeCAD.Vector(0, 35, 14)
            V2 = FreeCAD.Vector(0, 31, 14)
            V5 = FreeCAD.Vector(0, 4, 14)
            V6 = FreeCAD.Vector(0, 0, 14)
            V7 = FreeCAD.Vector(0, 0, 15)
            V8 = FreeCAD.Vector(0, 5, 15)
            V11 = FreeCAD.Vector(0, 30, 15)
            V12 = FreeCAD.Vector(0, 35, 15)
        V3 = FreeCAD.Vector(0, 31, 0)
        V4 = FreeCAD.Vector(0, 4, 0)
        V9 = FreeCAD.Vector(0, 5, 1)
        V10 = FreeCAD.Vector(0, 30, 1)

        L1 = Part.LineSegment(V1, V2)
        L2 = Part.LineSegment(V2, V3)
        L3 = Part.LineSegment(V3, V4)
        L4 = Part.LineSegment(V4, V5)
        L5 = Part.LineSegment(V5, V6)
        L6 = Part.LineSegment(V6, V7)
        L7 = Part.LineSegment(V7, V8)
        L8 = Part.LineSegment(V8, V9)
        L9 = Part.LineSegment(V9, V10)
        L10 = Part.LineSegment(V10, V11)
        L11 = Part.LineSegment(V11, V12)
        L12 = Part.LineSegment(V12, V1)
        S1 = Part.Shape([L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12])
        W = Part.Wire(S1.Edges)
        F = Part.Face(W)
        railLength = fp.Length
        P = F.extrude(FreeCAD.Vector(railLength, 0, 0))
        fp.Shape = P


class ViewProviderDINRailTS35:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
    def getIcon(self):
        return EB_Auxiliaries.workbenchFolderPath() + "\Icons\DINrailTS35.svg"

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"


def GetDINRailTS35(lenght=100):
    d = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DINRailTS35")
    d.Label = "TS35 DIN Rail"
    d.addProperty("App::PropertyFloat", "Length", "DIN Rail", "DIN rail length").Length = lenght
    d.addProperty("App::PropertyEnumeration", "Height", "DIN Rail", "DIN rail high").Height = ["7.5", "15"]
    d.addProperty("App::PropertyBool", "fixedPosition", "DIN Rail")
    DINRailTS35(d)
    ViewProviderDINRailTS35(d.ViewObject)
    f = FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup", "DINRail")
    f.addObject(d)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    return d
