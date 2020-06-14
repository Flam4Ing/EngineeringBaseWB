import EB_Auxiliaries
import clsConnectToEB
import clsEBObjectMaker
import FreeCAD
import FreeCADGui
import Part
import os
import Draft

class TerminalBlock:
    def __init__(self, obj):
         obj.Proxy = self

    def execute(self, fp):
        '''"Print a short message when doing a recomputation, this method is mandatory" '''
        sh = []
        stepFile = EB_Auxiliaries.TerminalBlocksPath() + "\\" + fp.TerminalType
        t = Part.Shape()
        t.read(stepFile)
        x = t.BoundBox.XMax
        y = t.BoundBox.YMax
        z = t.BoundBox.ZMax
        posText = FreeCAD.Vector(x,y,z)
        for x in range(fp.Quantity):
            tc = t.copy()
            tc.Placement.Base = FreeCAD.Vector(t.BoundBox.XLength*x,0,0)
            sh.append(tc)
        if len(fp.BMK) > 1:
            textObj = clsEBObjectMaker.GetTextObj(fp.BMK, fp.BMKsize)
            textObj.Placement.Base = (fp.BMKpos + posText)
            textObj.Placement.Rotation = FreeCAD.Rotation(FreeCAD.Vector(0,0,1),fp.BMKrot)
            sh.append(textObj)
        fp.Shape = Part.makeCompound(sh)

class ViewProviderTerminalBlock:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self
        obj.Transparency = 30
        obj.ShapeColor = (0.67,0.67,0.50)

    def getIcon(self):
        return EB_Auxiliaries.workbenchFolderPath() + "\Icons\Electrical_Terminal.svg"

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Flat Lines"

def GetTerminalBlock():
    d = clsEBObjectMaker.GetEBObjectMaker("TerminalBlock")
    d.Label = "Terminal block"
    d.addProperty("App::PropertyInteger","Quantity","Terminal Block Properties","Terminals quantity").Quantity = 1
    d.addProperty("App::PropertyEnumeration","TerminalType","Terminal Block Properties","Terminal type").TerminalType = os.listdir(EB_Auxiliaries.TerminalBlocksPath())
    TerminalBlock(d)
    ViewProviderTerminalBlock(d.ViewObject)
    if len(FreeCADGui.Selection.getSelection()) > 0:
        sel = FreeCADGui.Selection.getSelection()[0]
        #Add object to folder and select it
        parents = sel.InList
        for parent in parents:
            if parent.isDerivedFrom("App::DocumentObjectGroup"):
                parent.addObject(d)
        if "TS35" in sel.Name:
            if sel.Shape.BoundBox.XLength > sel.Shape.BoundBox.YLength:
                xShift = 5
                yShift = 17
                zShift = 0
            if sel.Shape.BoundBox.XLength < sel.Shape.BoundBox.YLength:
                xShift = -17
                yShift = 5
                zShift = 0
            vecShift = FreeCAD.Vector(xShift,yShift,zShift)
            vecSelection = sel.Placement.Base
            #d.Placement.Base = vecSelection + vecShift
            d.Placement.Base = sel.Shape.Vertexes[0].Point
            d.Placement.Rotation = sel.Placement.Rotation
    FreeCADGui.Selection.clearSelection()
    FreeCADGui.Selection.addSelection(d)
    FreeCAD.ActiveDocument.recompute()
    return d

def GetTerminalBlockFromEB():
    terminalProperties = clsConnectToEB.ConnectToEB().GetShapeProperties()
    d = GetTerminalBlock()
    d.Label = terminalProperties[0]
    d.Quantity = int(terminalProperties[8])
    d.BMK = terminalProperties[1]
    d.OID = terminalProperties[6]
    FreeCAD.ActiveDocument.recompute()
