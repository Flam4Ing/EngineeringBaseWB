import FreeCAD
import FreeCADGui
import Part
import os
import clsEBObjectMaker
import EB_Auxiliaries
import Utils.EB_Geometry

class DoorControls:
    def __init__(self, obj, folderPath):
        obj.Proxy = self
        self.objEB = obj
        self.STEPFolder = folderPath

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        sh = []
        self.facesByAreas = []
        sh.append(self.GetFrontPart())
        sh.append(self.GetBackPart())
        sh.append(self.GetTextBMK())
        fp.Shape = Part.makeCompound(sh)
        self.SetColorFrontPart()

    def GetFrontPart(self):
        frontPart = self.STEPFolder + "\\" + self.objEB.FileFrontPart
        f = Part.Shape()
        if os.path.isfile(frontPart):
            f.read(frontPart)

        """ Get faces to set colours"""
        for i in f.Faces:
            self.facesByAreas.append(i.Area)

        """ Get position for BMK text"""
        x = f.BoundBox.XMax
        y = f.BoundBox.YMax
        z = f.BoundBox.ZMax
        self.posText = FreeCAD.Vector(x, y, z)
        return f


    def GetBackPart(self):
        backPart = self.STEPFolder + "\\" + self.objEB.FileBackPart
        b = Part.Shape()
        if os.path.isfile(backPart):
            b.read(backPart)
        return b

    def GetTextBMK(self):
        t = Part.Shape()
        if len(self.objEB.BMK) > 1:
            textObj = clsEBObjectMaker.GetTextObj(self.objEB.BMK, self.objEB.BMKsize)
            textObj.Placement.Base = (self.objEB.BMKpos + self.posText)
            textObj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1),self.objEB.BMKrot)
            t = textObj
        return t


    def SetColorFrontPart(self):
        if str(self.objEB.FrontPartColour) == "Green":
            colour = (0., 1., 0.)
        if str(self.objEB.FrontPartColour) == "Red":
            colour = (1., 0., 0.)
        if str(self.objEB.FrontPartColour) == "Yellow":
            colour = (1.0, 1.0, 0.0)
        if str(self.objEB.FrontPartColour) == "White":
            colour = (1.0, 1.0, 1.0)
        defaultColour = (0.67,0.67,0.50)
        Utils.EB_Geometry.SetFaceColour(self.objEB, colour, defaultColour, self.facesByAreas, 0.01)

class ViewProviderDoorControls:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency = 20

    def getIcon(self):
        return EB_Auxiliaries.workbenchFolderPath() + "\Icons\IndicatorLight.svg"

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

def GetMatchesFiles(folderPath, criteria):
    """Get files wich contain criteria in name"""
    matchList = []
    fileList = os.listdir(folderPath)
    for i in fileList:
        if criteria in str(i):
            matchList.append(i)
    return matchList

def GetIndicatorLight():
    pathToIndicatorLights = EB_Auxiliaries.workbenchFolderPath()+ "\\StepFiles\\DoorControls\\IndicatorLights"
    d = clsEBObjectMaker.GetEBObjectMaker("IndicatorLight")
    d.Label = "Indicator Light"
    d.addProperty("App::PropertyEnumeration", "FileFrontPart", "Chose STEP File", "File for front part").FileFrontPart \
        = GetMatchesFiles(pathToIndicatorLights, "FrontPart")
    d.addProperty("App::PropertyEnumeration", "FileBackPart", "Chose STEP File","File for back part").FileBackPart \
        = GetMatchesFiles(pathToIndicatorLights, "BackPart")
    d.addProperty("App::PropertyEnumeration", "FrontPartColour", "Chose STEP File", "File for front part").FrontPartColour \
        =["Green", "Red", "Yellow", "White"]
    DoorControls(d, pathToIndicatorLights)
    ViewProviderDoorControls(d.ViewObject)
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    FreeCAD.ActiveDocument.recompute()
    return d

def GetDoorSwitches():
    pathToIndicatorLights = EB_Auxiliaries.workbenchFolderPath() + "\\StepFiles\\DoorControls\\Switches"
    d = clsEBObjectMaker.GetEBObjectMaker("DoorSwitch")
    d.Label = "DoorSwitch"
    d.addProperty("App::PropertyEnumeration", "FileFrontPart", "Chose STEP File", "File for front part").FileFrontPart \
        = GetMatchesFiles(pathToIndicatorLights, "FrontPart")
    d.addProperty("App::PropertyEnumeration", "FileBackPart", "Chose STEP File", "File for back part").FileBackPart \
        = GetMatchesFiles(pathToIndicatorLights, "BackPart")
    d.addProperty("App::PropertyEnumeration", "FrontPartColour", "Chose STEP File",
                  "File for front part").FrontPartColour \
        = ["Green", "Red", "Yellow", "White"]
    DoorControls(d, pathToIndicatorLights)
    ViewProviderDoorControls(d.ViewObject)
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    FreeCAD.ActiveDocument.recompute()
    return d