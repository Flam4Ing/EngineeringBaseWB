import FreeCAD
import FreeCADGui
import EB_Auxiliaries
import Draft

class RotateObject:
    def __init__(self, view):
        self.view = view
        self.i = 0
        self.callbackKey = self.view.addEventCallback("SoKeyboardEvent",self.PressedKey)
        print("Rotate selected object with keys 'X', 'Y', 'Z', 'ESCAPE' ")

    def PressedKey(self, info):
        #FreeCAD.Console.PrintMessage(str(info)+"\n") # list all events command
        if "Key" in info:
                keyDown = (info["Key"])
                if (keyDown.upper() == "X") and (info["State"] == "UP"):
                #if (keyDown.upper() == "R"):
                    #FreeCAD.Console.PrintMessage(str(keyDown)+"\n") # here the character pressed
                    v=FreeCAD.Vector(1,0,0)
                    self.Roatate(v)
                elif (keyDown.upper() == "Y") and (info["State"] == "UP"):
                    v=FreeCAD.Vector(0,1,0)
                    self.Roatate(v)
                elif (keyDown.upper() == "Z") and (info["State"] == "UP"):
                    v=FreeCAD.Vector(0,0,1)
                    self.Roatate(v)
                elif (keyDown.upper() == "ESCAPE"):
                    self.view.removeEventCallback("SoKeyboardEvent",self.callbackKey)
                    print("Rotate is escaped!")
    def Roatate(self, rotateAxis):
        if len(FreeCADGui.Selection.getSelection()) == 0:
            EB_Auxiliaries.MsgDialog ("Please select one object!")
            return
        
        sel = FreeCADGui.Selection.getSelection()[0]
        if len(sel.Shape.Solids) == 1:
            p = sel.Shape.Solids[0].CenterOfMass
        else:
            p = sel.Shape.Vertexes[0].Point
        Draft.rotate(sel, 90, p, axis=rotateAxis)

r = RotateObject(FreeCADGui.activeDocument().activeView())