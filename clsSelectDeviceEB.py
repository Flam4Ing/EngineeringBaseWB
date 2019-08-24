import WBAuxiliaries
import FreeCAD
import FreeCADGui
import subprocess

class SelectEBObject:
    def GetSelection(self):
        if len(FreeCADGui.Selection.getSelection()) == 0:
            WBAuxiliaries.MsgDialog("Please select EB device!")
            return
        sel = FreeCADGui.Selection.getSelection()[0]
        if str(type(sel)) == "<type 'FeaturePython'>" or str(type(sel)) == "<class 'FeaturePython'>":
            try:
                if WBAuxiliaries.testWithoutEB():
                    arguments = sel.OID + " " + "TESTwithoutEB"
                else:
                    arguments = sel.OID
                fileSelectDeviceInEB = WBAuxiliaries.scriptSelectShapeInEBPath()
                subprocess.call("wscript.exe " + fileSelectDeviceInEB + " " + arguments)
            except:
                WBAuxiliaries.MsgDialog("Please select EB device!")
        else:
            WBAuxiliaries.MsgDialog("Please select EB device!")

if __name__ == "__main__":
#    execfile("C:\Users\heinrich\AppData\Roaming\FreeCAD\Mod\!EBase\clsSelectEBObject.py")
    eB = SelectEBObject()
    eB.GetSelection()
