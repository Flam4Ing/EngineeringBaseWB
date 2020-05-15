import EB_Auxiliaries
import FreeCAD
import FreeCADGui
import subprocess

class SelectEBObject:
    def GetSelection(self):
        if len(FreeCADGui.Selection.getSelection()) == 0:
            EB_Auxiliaries.MsgDialog("Please select EB device!")
            return
        sel = FreeCADGui.Selection.getSelection()[0]
        if hasattr(sel, "OID"):
            try:
                if EB_Auxiliaries.testWithoutEB():
                    arguments = sel.OID + " " + "TESTwithoutEB"
                else:
                    arguments = sel.OID

                fileSelectDeviceInEB = EB_Auxiliaries.scriptSelectShapeInEBPath()
                subprocess.call("wscript.exe " + fileSelectDeviceInEB + " " + arguments)
            except:
                EB_Auxiliaries.MsgDialog("Please select EB device!")
        else:
            EB_Auxiliaries.MsgDialog("Please select EB device!")