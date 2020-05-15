import EB_Auxiliaries
import FreeCAD
import os
import subprocess
import sys


class ConnectToEB:

    def GetShapeProperties(self):
        self.LetWriteFileFromEB()
        self.ReadFileFromEB()
        return self.shapeProperties

    def LetWriteFileFromEB(self):
        import subprocess
        if EB_Auxiliaries.testWithoutEB():
            arguments = EB_Auxiliaries.vbsScriptsPath() + " " + "TESTwithoutEB"
        else:
            arguments = EB_Auxiliaries.vbsScriptsPath()

        fileGetEBShape = EB_Auxiliaries.scriptGetEBShapePath()
        # subprocess.call("wscript.exe C:\Users\heinrich\Desktop\GetEBshape.vbs " + arg)
        subprocess.call("wscript.exe " + fileGetEBShape + " " + arguments)

    def ReadFileFromEB(self):
        fileEBshapeExported = EB_Auxiliaries.textEBShapeExportedPath()
        if sys.version_info.major < 3:
            with open(fileEBshapeExported) as f:
                content = f.readlines()
        else:
            with open(fileEBshapeExported, encoding="utf-8") as f:
                content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        self.shapeProperties = [x.strip() for x in content]

