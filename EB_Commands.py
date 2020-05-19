import EB_Auxiliaries
import FreeCAD
import FreeCADGui
import Utils.EB_Geometry


class Get_EB_Shape():
    """My new command"""

    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\ButtonDown.svg",
                # the name of a svg file available in the resources
                'Accel': "Shift+S",  # a default shortcut (optional)
                'MenuText': "Get device from EB"}

    def Activated(self):
        """Do something here"""
        import DraftExtentions
        DraftExtentions.PlaceDeviceOnPoint().Activated("Box")
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Get_EB_Shape_Step():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\ButtonDown_.svg",
                # the name of a svg file available in the resources
                'MenuText': "Get device from EB as Step"}

    def Activated(self):
        """Do something here"""
        import DraftExtentions
        DraftExtentions.PlaceDeviceOnPoint().Activated("Step")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Add_EB_Shape_With_Shift():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Add.svg",
                # the name of a svg file available in the resources
                'MenuText': "Add device from EB with shift"}

    def Activated(self):
        """Do something here"""
        import clsGetDeviceEB
        clsGetDeviceEB.AddEBDeviceWithShift()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Add_EB_Shape_With_Shift_Step():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Add_.svg",
                # the name of a svg file available in the resources
                'MenuText': "Add device from EB with shift as step"}

    def Activated(self):
        """Do something here"""
        import clsGetDeviceEB
        clsGetDeviceEB.AddEBDeviceWithShift(True)
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Add_EB_Step_Assembly():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Add_Step_Assembly.svg",
                # the name of a svg file available in the resources
                'MenuText': "Add device from EB as step assembly"}

    def Activated(self):
        """Do something here"""
        import clsGetDeviceEB
        clsGetDeviceEB.GetSTEPAssembly()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Select_EB_Shape():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\ButtonUp.svg",
                # the name of a svg file available in the resources
                'MenuText': "Select Device in EB"}

    def Activated(self):
        """Do something here"""
        import clsSelectDeviceEB
        ebD = clsSelectDeviceEB.SelectEBObject()
        ebD.GetSelection()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Clear_Console():

    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Delete.svg",
                # the name of a svg file available in the resources
                'MenuText': "Clear Console"}

    def Activated(self):
        import EB_Auxiliaries
        import subprocess
        fileDeletePYCfiles = EB_Auxiliaries.scriptDeletePYCfilesPath()
        subprocess.call("wscript.exe " + fileDeletePYCfiles)

        import PySide
        from PySide import QtGui
        mw = FreeCAD.Gui.getMainWindow()
        try:
            c = mw.findChild(QtGui.QPlainTextEdit, "Python console")
            c.clear()
        except Exception:
            None
        try:
            r = mw.findChild(QtGui.QTextEdit, "Report view")
            r.clear()
        except Exception:
            None

    def IsActive(self):
        return True


class Get_DIN_Rail_TS35():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\TS35.png",
                'MenuText': "Get DIN rail TS35"}

    def Activated(self):
        """Do something here"""
        import DraftExtentions
        DraftExtentions.PlaceDeviceOnPoint().Activated("TS35")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Get_Terminal_Block():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Terminal.png",
                'MenuText': "Get terminal block"}

    def Activated(self):
        """Do something here"""
        import clsTerminalBlock
        clsTerminalBlock.GetTerminalBlock()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Get_GuiTab():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Simple.svg",
                'MenuText': "Get GuiTab"}

    def Activated(self):
        """Do something here"""
        import EB_GuiCommandTab
        EB_GuiCommandTab.CreateGui()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Move_Point_To_Point():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Draft_Move.svg",
                'MenuText': "Move object by point to point"}

    def Activated(self):
        """Do something here"""
        # from Commands import mPoinToPoint
        # mPoinToPoint.DoIt()
        EB_Auxiliaries.RunCommand("mPoinToPoint.py")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Mover_For_Object():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\mMove.png",
                'MenuText': "Move object"}

    def Activated(self):
        """Do something here"""
        objToMove = FreeCADGui.Selection.getSelection()[0]
        FreeCADGui.ActiveDocument.setEdit(objToMove, 0)
        return

    def IsActive(self):
        # if FreeCADGui.ActiveDocument:
        if len(FreeCADGui.Selection.getSelection()) > 0:
            return True
        else:
            return False


class Set_Display_Mode_Wire_Frame():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Visibility_WireFrame.png",
                'MenuText': "Set display mode wireframe"}

    def Activated(self):
        """Do something here"""
        EB_Auxiliaries.RunCommand("VisibilitySetWireframe.py")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Set_Display_Mode_Flat_Lines():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Visibility_FlatLines.png",
                'MenuText': "Set display mode wireframe"}

    def Activated(self):
        """Do something here"""
        EB_Auxiliaries.RunCommand("VisibilitySetFlatLines.py")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Set_Transparancy():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Visibility_Transparency.svg",
                'MenuText': "Set transparency"}

    def Activated(self):
        """Do something here"""
        EB_Auxiliaries.RunCommand("VisibilitySetTransparency.py")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Set_Visibility_True():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Visibility_True.svg",
                'MenuText': "Set visibility true"}

    def Activated(self):
        """Do something here"""
        EB_Auxiliaries.RunCommand("VisibilitySetTrue.py")
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class Rotate_Sel_Object_15():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Rotate90.svg",
                'MenuText': "Rotate 15",
                'ToolTip': 'Auxiliary tool to rotate a shape 15 degrees.\nSelect a face or edge of the object you want to rotate\n and it will be rotated 15 degrees using its normal as rotation\n axis'}

    def Activated(self):
        """Do something here"""
        sel = FreeCADGui.Selection.getSelectionEx()
        if len(sel) == 0:
            EB_Auxiliaries.MsgDialog("Please select face or edge of shape!")
            return
        if "Face" in str(sel[0].SubObjects[0]):
            selFace = sel[0].SubObjects[0]
            rot_center = selFace.CenterOfMass
            rot_axis = selFace.normalAt(0, 0)
        elif "Edge" in str(sel[0].SubObjects[0]):
            selEdge = sel[0].SubObjects[0]
            rot_center = Utils.EB_Geometry.centerLinePoint(selEdge)
            rot_axis = Utils.EB_Geometry.edgeToVector(selEdge)
        else:
            EB_Auxiliaries.MsgDialog("Please select face or edge of shape!")
            return
        objA = sel[0].Object
        rot = FreeCAD.Rotation(rot_axis, 15)
        objA.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 0), rot, rot_center).multiply(objA.Placement)
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class EnableConnectionToEB():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\ConnectionToEB.svg",
                'MenuText': "Enable connection to EB",
                'ToolTip': 'Enable connection to EB'}

    def Activated(self):
        """Do something here"""
        # Test workbench without Ingeneering Base installation
        FreeCAD.testWithOutEB = False
        return

    def IsActive(self):
        if FreeCAD.testWithOutEB:
            return True
        else:
            return False

class DisableConnectionToEB():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\TestMode.svg",
                'MenuText': "Disable connection to EB",
                'ToolTip': 'Disable connection to EB'}

    def Activated(self):
        """Do something here"""
        # Test workbench without Ingeneering Base installation
        FreeCAD.testWithOutEB = True
        return

    def IsActive(self):
        if FreeCAD.testWithOutEB:
            return False
        else:
            return True

class ShowTestsConsole():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\ShowTestsConsole.svg",
                'MenuText': "Show Tests Console",
                'ToolTip': 'ShowTestsConsole'}

    def Activated(self):
        """Do something here"""
        # Test workbench without Ingeneering Base installation
        import EB_GuiTestTab
        EB_GuiTestTab.CreateGui()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


FreeCADGui.addCommand('Clear_Console', Clear_Console())
FreeCADGui.addCommand('Get_EB_Shape', Get_EB_Shape())
FreeCADGui.addCommand('Get_EB_Shape_Step', Get_EB_Shape_Step())
FreeCADGui.addCommand('Add_EB_Shape_With_Shift', Add_EB_Shape_With_Shift())
FreeCADGui.addCommand('Add_EB_Shape_With_Shift_Step', Add_EB_Shape_With_Shift_Step())
FreeCADGui.addCommand('Add_EB_Step_Assembly', Add_EB_Step_Assembly())
FreeCADGui.addCommand('Select_EB_Shape', Select_EB_Shape())
FreeCADGui.addCommand('Get_DIN_Rail_TS35', Get_DIN_Rail_TS35())
FreeCADGui.addCommand('Get_Terminal_Block', Get_Terminal_Block())
FreeCADGui.addCommand('Get_GuiTab', Get_GuiTab())
FreeCADGui.addCommand('Move_Piont_To_Point', Move_Point_To_Point())
FreeCADGui.addCommand('Mover_For_Object', Mover_For_Object())
FreeCADGui.addCommand('Set_Display_Mode_Wire_Frame', Set_Display_Mode_Wire_Frame())
FreeCADGui.addCommand('Set_Display_Mode_Flat_Lines', Set_Display_Mode_Flat_Lines())
FreeCADGui.addCommand('Set_Transparancy', Set_Transparancy())
FreeCADGui.addCommand('Set_Visibility_True', Set_Visibility_True())
FreeCADGui.addCommand('Rotate_Sel_Object_15', Rotate_Sel_Object_15())
FreeCADGui.addCommand('EnableConnectionToEB', EnableConnectionToEB())
FreeCADGui.addCommand('DisableConnectionToEB', DisableConnectionToEB())
FreeCADGui.addCommand('ShowTestsConsole', ShowTestsConsole())
