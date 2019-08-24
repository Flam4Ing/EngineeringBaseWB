import WBAuxiliaries
import FreeCAD
import FreeCADGui
import Part

class WiringDuct:
    def __init__(self, obj):
        obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        P = Part.makeBox(fp.Length, fp.Height, fp.Width)
        fp.Shape = P

class ViewProviderWiringDuct:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency = 20

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

def GetWiringDuct(lenght = 100, height = 50, width = 50):
    d=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","DINRailTS35")
    d.Label = "Wiring duct"
    d.addProperty("App::PropertyFloat","Length","Wiring Duct","Wiring duct length").Length = lenght
    d.addProperty("App::PropertyFloat","Height","Wiring Duct","Wiring duct high").Height = height
    d.addProperty("App::PropertyFloat","Width","Wiring Duct","Wiring duct high").Width = width
    WiringDuct(d)
    ViewProviderWiringDuct(d.ViewObject)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    return d


if __name__ == "__main__":
# execfile("C:\Users\heinrich\Desktop\FreeCAD18\Mod\!EngineeringBase\clsWiringDuct.py")
    GetWiringDuct()