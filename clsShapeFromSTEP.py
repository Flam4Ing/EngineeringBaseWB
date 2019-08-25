import FreeCAD
import FreeCADGui
import Part
import os
import WBAuxiliaries
#Test

class ShapeFromSTEP:
    def __init__(self, obj, folderPath):
         obj.Proxy = self
         self.STEPFolder = folderPath

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        stepFile = self.STEPFolder + "\\" + fp.STEPFile
        t = Part.Shape()
        t.read(stepFile)
        fp.Shape = t

class ViewProviderShapeFromSTEP:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency = 20

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

def GetShapeFromSTEP(shapeName = "ShapeFromSTEP", folderPath = " "):
    d=FreeCAD.ActiveDocument.addObject("Part::FeaturePython",shapeName)
    d.Label = shapeName
    d.addProperty("App::PropertyEnumeration","STEPFile","Chose STEP File","STEP File").STEPFile = os.listdir(folderPath)
    ShapeFromSTEP(d, folderPath)
    ViewProviderShapeFromSTEP(d.ViewObject)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    return d


if __name__ == "__main__":
# execfile("C:\Users\heinrich\Desktop\FreeCAD18\Mod\!EngineeringBase\clsWiringDuct.py")
    #GetShapeFromSTEP()
    pass
