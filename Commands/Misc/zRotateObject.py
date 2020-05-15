import FreeCAD
import FreeCADGui
import EB_Auxiliaries

class RotateObject:
    def __init__(self, view):
        self.view = view
        self.i = 0
        self.callbackKey = self.view.addEventCallback("SoKeyboardEvent",self.PressedKey)

    def PressedKey(self, info):
        #FreeCAD.Console.PrintMessage(str(info)+"\n") # list all events command
        if "Key" in info:
                keyDown = (info["Key"])
                if (keyDown.upper() == "R") and (info["State"] == "UP"):
                #if (keyDown.upper() == "R"):
                    #FreeCAD.Console.PrintMessage(str(keyDown)+"\n") # here the character pressed
                    self.Roatate()
                elif (keyDown.upper() == "ESCAPE"):
                    self.view.removeEventCallback("SoKeyboardEvent",self.callbackKey)

    def Roatate(self):
        if len(FreeCADGui.Selection.getSelection()) == 0:
            EB_Auxiliaries.MsgDialog ("Please select one object!")
            return
        
        rot = [FreeCAD.Rotation(90,0,0),
                FreeCAD.Rotation(-90,0,0),
                FreeCAD.Rotation(90,0,90),
                FreeCAD.Rotation(-90,0,-90),
                FreeCAD.Rotation(90,90,90),
                FreeCAD.Rotation(-90,-90,-90),
                FreeCAD.Rotation(0,-90,0),
                FreeCAD.Rotation(90,-90,-90),
                FreeCAD.Rotation(0,0,0)
            ]
        
        sel = FreeCADGui.Selection.getSelection()[0]
        sel.Placement.Rotation = rot[self.i]
        self.i += 1
        if self.i == len(rot):
            self.i = 0

r = RotateObject(FreeCADGui.activeDocument().activeView())