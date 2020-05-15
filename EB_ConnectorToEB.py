import EB_Auxiliaries
import sys


class ExportedDeviceFromEB:
    def __init__(self):
        self.Label = ""
        self.BMK = ""
        self.PathToSTEPfile = ""
        self.BoxWidth = 0
        self.BoxHeight = 0
        self.BoxDepth = 0
        self.OID = ""
        self.DeviceName = ""
        self.TerminalsNumber = 0
        self.LetWriteFileWithDeviceInfoFromEB()
        self.ReadExportedFileFromEB()


    def LetWriteFileWithDeviceInfoFromEB(self):
        """VBScript receives the path as an argument
            and writes the txt-file to a given folder.
            If VBScript receives to arguments, then no connection to EB"""
        import subprocess
        if EB_Auxiliaries.testWithoutEB():
            arguments = EB_Auxiliaries.vbsScriptsPath() + " " + "TESTwithoutEB"
        else:
            arguments = EB_Auxiliaries.vbsScriptsPath()

        fileGetEBShape = EB_Auxiliaries.scriptGetEBShapePath()
        # subprocess.call("wscript.exe C:\Users\heinrich\Desktop\GetEBshape.vbs " + arg)
        subprocess.call("wscript.exe " + fileGetEBShape + " " + arguments)

    def ReadExportedFileFromEB(self):
        fileEBshapeExported = EB_Auxiliaries.textEBShapeExportedPath()
        if sys.version_info.major < 3:
            with open(fileEBshapeExported) as f:
                content = f.readlines()
        else:
            with open(fileEBshapeExported, encoding="utf-8") as f:
                content = f.readlines()
        shapeProperties = [x.strip() for x in content]
        self.Label = shapeProperties[0]
        self.BMK = shapeProperties[1]
        self.PathToSTEPfile = shapeProperties[2]
        self.BoxWidth = float (shapeProperties[3])
        self.BoxHeight = float (shapeProperties[4])
        self.BoxDepth = float (shapeProperties[5])
        self.OID = shapeProperties[6]
        self.DeviceName = shapeProperties[7]
        self.TerminalsNumber = int (shapeProperties[8])


if __name__ == "__main__":
    d = ExportedDeviceFromEB()
    print(d.Label)
    print(d.BMK)
    print(d.PathToSTEPfile)
    print(str(d.BoxWidth))