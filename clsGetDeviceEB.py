import EB_Auxiliaries
import clsConnectToEB
import clsEBObjectMaker
import FreeCAD
import FreeCADGui
import ImportGui
import Part
import os
import sys

class EBDevice:
    def __init__(self, obj, Step=False):
         obj.Proxy = self
         self.isSTEP = Step
    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        sh = []
        if self.isSTEP:
            deviceObj = Part.Shape()
            deviceObj.read(fp.STEPfile)
        else:
            posDevice = FreeCAD.Vector(0,-(fp.BoxHeight/2+17), -6)
            deviceObj = Part.makeBox(fp.BoxWidth,fp.BoxHeight,fp.BoxDepth, posDevice)
        posLine = Part.makeLine(deviceObj.Placement.Base, 
                          (deviceObj.Placement.Base.x+deviceObj.BoundBox.XLength+0.333, 
                            deviceObj.Placement.Base.y, deviceObj.Placement.Base.z))
        sh.append(posLine)
        sh.append(deviceObj)
        fp.EBShape = deviceObj #add shape to object property
        fp.PositionLine = posLine #Line to find position
        shCenter = deviceObj.BoundBox.Center
        x = shCenter.x
        y = shCenter.y
        z = deviceObj.BoundBox.ZMax+1
        posText = FreeCAD.Vector(x,y,z)
        if len(fp.BMK) > 1:
            textObj = clsEBObjectMaker.GetTextObj(fp.BMK, fp.BMKsize)
            textObj.Placement.Base = (fp.BMKpos + posText)
            textObj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1),fp.BMKrot)
            sh.append(textObj)

        fp.Shape = Part.makeCompound(sh)

class ViewProviderEBDevice:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency = 20

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

def GetEBDevice(stepShape=False):
    deviceProperties = clsConnectToEB.ConnectToEB().GetShapeProperties()
    if float(deviceProperties[3]) == 0 or float(deviceProperties[4]) == 0 or float(deviceProperties[5]) == 0:
        EB_Auxiliaries.MsgDialog("Width or Height or Depth from Device is null!")
        return #Keine Bemassung in EB
    d = clsEBObjectMaker.GetEBObjectMaker("EBDevice")
    d.addProperty("App::PropertyFloat","BoxWidth","Engineering Base Information","Device width").BoxWidth = float(deviceProperties[3])
    d.addProperty("App::PropertyFloat","BoxHeight","Engineering Base Information","Device Height").BoxHeight = float(deviceProperties[4])
    d.addProperty("App::PropertyFloat","BoxDepth","Engineering Base Information","Device length").BoxDepth = float(deviceProperties[5])
    d.Label = deviceProperties[0]
    d.ADevice = deviceProperties[7]
    d.BMK = deviceProperties[1]
    d.BMKrot = 90
    d.STEPfile = deviceProperties[2]
    d.OID = deviceProperties[6]
    exists = os.path.isfile(deviceProperties[2])
    if ((not exists) and stepShape):
        print ("STEP file doesn't exist!")
    EBDevice(d, (exists and stepShape))
    ViewProviderEBDevice(d.ViewObject)
    FreeCAD.ActiveDocument.recompute()
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)

    #print (d.PositionLine.Placement)
    return d

def AddEBDeviceWithShift(stepShape=False):
    if len(FreeCADGui.Selection.getSelection()) == 0:
        EB_Auxiliaries.MsgDialog ("Please select EB device!")
        return
    sel = FreeCADGui.Selection.getSelection()[0]
    
    if str(type(sel)) == "<class 'FeaturePython'>" or str(type(sel)) == "<type 'FeaturePython'>":
        #try:
            vecSelection = sel.Placement.Base
            d = GetEBDevice(stepShape)
            #Add object to folder and select it
            parents = sel.InList
            for parent in parents:
                if parent.isDerivedFrom("App::DocumentObjectGroup"):
                    parent.addObject(d)
            FreeCADGui.Selection.clearSelection()
            FreeCADGui.Selection.addSelection(d)
            #Place on DIN Rail
            if "TS35" in sel.Name:
                d.Placement.Base = sel.Shape.Vertexes[0].Point
                d.Placement.Rotation = sel.Placement.Rotation
                return
            #Place it as next object
            #xShift = sel.EBShape.BoundBox.XLength
            #YawZ = sel.Placement.Rotation.toEuler()[0]
            #PitchY = sel.Placement.Rotation.toEuler()[1]
            #RollX  = sel.Shape.Placement.Rotation.toEuler()[2]
            #vecShift = FreeCAD.Vector(xShift,0,0)
            #d.Placement.Base = vecShift + sel.Placement.Base
            d.Placement.Rotation = sel.Placement.Rotation
            for l in sel.Shape.Edges:
                if l.Length == sel.PositionLine.Length:
                    vecShift = l.Vertexes[1].Point
            d.Placement.Base = vecShift
        #except:
            #print("Failure to place the EB device!")
    else:
        EB_Auxiliaries.MsgDialog ("Please select EB device!")

def GetSTEPAssembly():
    deviceProperties = clsConnectToEB.ConnectToEB().GetShapeProperties()
    file_path = deviceProperties[2]
    exists = os.path.isfile(file_path)
    if exists:
        ImportGui.insert(file_path, FreeCAD.ActiveDocument.Name)
    else:
        EB_Auxiliaries.MsgDialog("STEP file doesn't exist!")

