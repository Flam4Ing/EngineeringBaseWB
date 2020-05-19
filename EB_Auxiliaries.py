from PySide import QtCore, QtGui
import os
import sys
import FreeCADGui
import FreeCAD

#------------------------------------------------------------------------------
def testWithoutEB():
    # Test workbench without Ingeneering Base installation
    return True
    # return False


# ------Pathes of Files
# workbenchFolder = os.path.dirname(os.path.realpath(__file__))
# workbenchFolder = FreeCAD.__path__[3] + "\!EBase"
#------------------------------------------------------------------------------
def workbenchFolderPath():
    return os.path.dirname(os.path.realpath(__file__))

#------------------------------------------------------------------------------
def fontFilePath():
    return workbenchFolderPath() + "\\VBScripts\\arial.ttf"

#------------------------------------------------------------------------------
def scriptGetEBShapePath():
    return workbenchFolderPath() + "\\VBScripts\\GetDeviceEB.vbs"

#------------------------------------------------------------------------------
def textEBShapeExportedPath():
    return workbenchFolderPath() + "\\VBScripts\\ExportedDeviceEB.txt"

#------------------------------------------------------------------------------
def vbsScriptsPath():
    return workbenchFolderPath() + "\\VBScripts"

#------------------------------------------------------------------------------
def scriptSelectShapeInEBPath():
    return workbenchFolderPath() + "\\VBScripts\\SelectDeviceInEB.vbs"

#------------------------------------------------------------------------------
def scriptDeletePYCfilesPath():
    return workbenchFolderPath() + "\\DeletePYCfiles.vbs"

#------------------------------------------------------------------------------
def IpSettingsPath():
    return workbenchFolderPath() + "\\VBScripts\\IpSettings.txt"

#------------------------------------------------------------------------------
def autoItExePath():
    return workbenchFolderPath() + "\\VBScripts\\AutoIt3.exe"

#------------------------------------------------------------------------------
def scriptHotKeysPath():
    return workbenchFolderPath() + "\\VBScripts\\SendCommandToFreeCAD.au3"

#------------------------------------------------------------------------------
def TerminalBlocksPath():
    return workbenchFolderPath() + "\\" + "TerminalBlocks"

#------------------------------------------------------------------------------
def CableGlandsPath():
    return workbenchFolderPath() + "\\" + "CableGlands"

#------------------------------------------------------------------------------
def RunCommand(fileName):
    '''Run in console py-files in folder Commands'''
    import FreeCADGui
    filePath = workbenchFolderPath() + "\\Commands\\" + fileName
    filePath = filePath.replace('\\', '/')
    if sys.version_info.major < 3:
        command = 'execfile("' + filePath + '")'
    else:
        # exec(compile(open(file).read(), file, 'exec'))
        command = 'exec(compile(open("' + filePath + '", encoding="utf-8").read(),"' + filePath + '", "exec"))'
    FreeCADGui.doCommand(command)

#------------------------------------------------------------------------------
def MsgDialog(msg):
    # Create a simple dialog QMessageBox
    # The first argument indicates the icon used: one of QtGui.QMessageBox.{NoIcon, Information, Warning, Critical, Question} 
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Attention!", msg)
    diag.setWindowModality(QtCore.Qt.ApplicationModal)
    diag.exec_()

#------------------------------------------------------------------------------
def GetSelectionWithSubObjects():
    selList = []

    """recursive function"""
    def GetSubelements(groupObj):
        children = groupObj.OutList
        for c in children:
            if not (c.isDerivedFrom('App::DocumentObjectGroup') or c.isDerivedFrom('App::Part')):
                selList.append(c)
            else:
                GetSubelements(c)
    """end recursive function"""
    
    if len(FreeCADGui.Selection.getSelection()) != 0:
        selObjects = FreeCADGui.Selection.getSelection()
        for o in selObjects:
            if not (o.isDerivedFrom('App::DocumentObjectGroup') or o.isDerivedFrom('App::Part')):
                selList.append(o)
            else:
                GetSubelements(o)
    return selList
#------------------------------------------------------------------------------
def GetChildrenFromObject(parentObject):
    selList = []

    """recursive function"""
    def GetSubelements(groupObj):
        children = groupObj.OutList
        for c in children:
            if not (c.isDerivedFrom('App::DocumentObjectGroup') or c.isDerivedFrom('App::Part')):
                selList.append(c)
            else:
                GetSubelements(c)
    """end recursive function"""

    if not (parentObject.isDerivedFrom('App::DocumentObjectGroup') or parentObject.isDerivedFrom('App::Part')):
        selList.append(parentObject)
    else:
        GetSubelements(parentObject)
    return selList
    
    
#------------------------------------------------------------------------------
class SelectionGate(object):
    '''To set selection filter - Face, Edge, Vertex
    g = SelectionGate("Face")
    FreeCADGui.Selection.addSelectionGate(g)
       To delete selection filter
    FreeCADGui.Selection.removeSelectionGate()'''
    def __init__(self, selectFilter):
        self.toSelect = selectFilter

    def allow(self, doc, obj, sub):
        if not obj.isDerivedFrom("Part::Feature"):
            return False
        if str(sub).startswith(self.toSelect):
            return True
        return False

#------------------------------------------------------------------------------
def DeleteObjectbyLabel(obj):
    try:
        FreeCAD.getDocument(str(FreeCAD.activeDocument().Name)).removeObject(obj.Label)
    except:
        pass
#------------------------------------------------------------------------------
def a_clear_console():
    '''clearing previous messages in Python console and Report view'''
    mw = FreeCADGui.getMainWindow()
    c = mw.findChild(QtGui.QPlainTextEdit, "Python console")
    c.clear()
    r = mw.findChild(QtGui.QTextEdit, "Report view")
    r.clear()
