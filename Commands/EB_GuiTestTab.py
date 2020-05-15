import os
import sys
import glob
from PySide import QtCore, QtGui
import FreeCAD
import EB_Auxiliaries

pathToIcons = EB_Auxiliaries.workbenchFolderPath() + "\\" + "Icons"
iconsPNG = glob.glob1(pathToIcons, "*.png")
iconsSVG = glob.glob1(pathToIcons, "*.svg")
iconsPNG.extend(iconsSVG)


def createDockWindows(mWindow):
    dock = QtGui.QDockWidget("Run Tests", mWindow)
    centralWidget = QtGui.QWidget(dock)
    centralWidget.setObjectName(("centralWidget"))
    centralWidget.setGeometry(10, 10, 150, 300)

    # Listview
    listWidget = QtGui.QListWidget(centralWidget)
    listWidget.setFixedSize(300, 450)
    listWidget.setStyleSheet(
        "QListWidget::item { border: 1px dotted gray} QListWidget::item:selected {background: grey}")
    # listWidget.setStyleSheet("QListWidget::item {background: white; border: 1px solid gray}")
    # listWidget.setStyleSheet("QListWidget::item:selected {background: grey}")

    # QtGui.QListWidgetItem(listWidget)
    # for i in range(10):
    # item = QtGui.QListWidgetItem("Item %i" % i)
    # listWidget.addItem(item)
    # listWidget.itemClicked.connect(Clicked)
    # fileList = os.listdir(WBSettings.workbenchFolderPath())
    fileList = glob.glob1(EB_Auxiliaries.workbenchFolderPath(), "*.py")

    for fileName in fileList:
        item = QtGui.QListWidgetItem(fileName)
        iconPath = pathToIcons + "\\zScriptDefault.svg"
        for icon in iconsPNG:
            index_of_dot = fileName.index('.')
            file_name_without_extension = fileName[:index_of_dot]

            if file_name_without_extension in icon:
                iconPath = pathToIcons + "\\" + icon

        item.setIcon(QtGui.QIcon(iconPath))
        # item.setBackground( QtGui.QColor("gray") )
        listWidget.addItem(item)

    # self.listWidget.addItems(fileList)
    listWidget.setIconSize(QtCore.QSize(30, 30))
    listWidget.itemDoubleClicked.connect(Clicked)



    dock.setWidget(centralWidget)
    mWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)


def Clicked(item):
    import FreeCADGui as Gui
    filePath = EB_Auxiliaries.workbenchFolderPath() + "\\" + item.text()
    # print(filePath)
    filePath = filePath.replace('\\', '/')
    if sys.version_info.major < 3:
        command = 'execfile("' + filePath + '")'
    else:
        # exec(compile(open(file).read(), file, 'exec'))
        command = 'exec(compile(open("' + filePath + '", encoding="utf-8").read(),"' + filePath + '", "exec"))'
    Gui.doCommand(command)




def CreateGui():
    mWindow = FreeCAD.Gui.getMainWindow()
    createDockWindows(mWindow)

CreateGui()
