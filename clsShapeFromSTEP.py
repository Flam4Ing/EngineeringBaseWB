import FreeCAD
import FreeCADGui
import Part
import os
import ImportGui
import EB_Auxiliaries

class ShapeFromSTEP:
    def __init__(self, obj, folderPath):
        obj.Proxy = self
        self.STEPFolder = folderPath

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        stepFilePath = self.STEPFolder + "\\" + fp.STEPFile

        if fp.IsWithColour:
            self.GetShapeWithColor(fp, stepFilePath)
        else:
            self.GetShapeWithoutColor(fp, stepFilePath)


    def GetShapeWithColor(self, fp, stepFilePath):
        doc = FreeCAD.ActiveDocument
        current_instances = set(doc.findObjects())
        ImportGui.insert(stepFilePath, doc.Name)
        new_instances = list(set(doc.findObjects()) - current_instances)
        if not len(new_instances) == 1:
            self.DeleteObjects(doc, new_instances)
            print("In step file are more as one shapes!")
            self.GetShapeWithoutColor(fp, stepFilePath)
        else:
            print("In step file is one shape!")
            newObj = new_instances[0]
            fp.Shape = newObj.Shape
            fp.ViewObject.ShapeColor = newObj.ViewObject.ShapeColor
            fp.ViewObject.DiffuseColor = newObj.ViewObject.DiffuseColor
            self.DeleteObjects(doc, new_instances)


    def GetShapeWithoutColor(self, fp, stepFilePath):
        t = Part.Shape()
        t.read(stepFilePath)
        fp.Shape = t
        # fp.ViewObject.ShapeColor = (0.67, 0.67, 0.50)
        fp.ViewObject.ShapeColor = fp.ViewObject.ShapeColor

    def DeleteObjects(self, doc, objects):
        for s in objects:
            try:
                # if not doc.getObject(s.Name) == None:
                doc.removeObject(s.Name)
            except:
                pass


class ViewProviderShapeFromSTEP:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency = 5

    def getIcon(self):
        return EB_Auxiliaries.workbenchFolderPath() + "\Icons\EB_Device.svg"

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

def GetShapeFromSTEP(shapeName = "ShapeFromSTEP", folderPath = " "):
    d=FreeCAD.ActiveDocument.addObject("Part::FeaturePython",shapeName)
    d.Label = shapeName
    d.addProperty("App::PropertyEnumeration","STEPFile","Chose STEP File","STEP File").STEPFile = os.listdir(folderPath)
    d.addProperty("App::PropertyBool", "IsWithColour", "Chose STEP File", "STEP with colour").IsWithColour = False
    ShapeFromSTEP(d, folderPath)
    ViewProviderShapeFromSTEP(d.ViewObject)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    return d

