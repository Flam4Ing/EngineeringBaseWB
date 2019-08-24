import os
import sys
import glob
from functools import partial
from PySide import QtCore, QtGui
import FreeCAD
import WBAuxiliaries

pathToIcons = WBAuxiliaries.workbenchFolderPath() + "\\" + "Commands"
iconList = glob.glob1(pathToIcons, "*.png")
iconList1 = glob.glob1(pathToIcons, "*.svg")
iconList.extend(iconList1)


def createDockWindows(mWindow):
    dock = QtGui.QDockWidget("Scripts", mWindow)
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
    fileList = glob.glob1(WBAuxiliaries.workbenchFolderPath() + "\\" + "Commands", "*.py")

    for fileName in fileList:
        item = QtGui.QListWidgetItem(fileName)
        iconPath = pathToIcons + "\\zScriptDefault.svg"
        for icon in iconList:
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

    # Button Move
    btn01 = QtGui.QPushButton(centralWidget)
    btn01.setGeometry(0, 455, 100, 40)
    # pushButton01.clicked.connect(partial(ButtonClick,listWidget))
    btn01.clicked.connect(lambda: filterList(listWidget, "m"))
    btn01.setText("Move")

    # Button Place
    btn02 = QtGui.QPushButton(centralWidget)
    btn02.setGeometry(100, 455, 100, 40)
    btn02.clicked.connect(lambda: filterList(listWidget, "Place"))
    btn02.setText("Place")

    # Button Visibility
    btn03 = QtGui.QPushButton(centralWidget)
    btn03.setGeometry(200, 455, 100, 40)
    btn03.clicked.connect(lambda: filterList(listWidget, "Visibi"))
    btn03.setText("Visibility")

    # Button All
    btn10 = QtGui.QPushButton(centralWidget)
    btn10.setGeometry(200, 495, 100, 40)
    btn10.clicked.connect(lambda: filterList(listWidget, ""))
    btn10.setText("ALL")

    dock.setWidget(centralWidget)
    mWindow.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)


def Clicked(item):
    import FreeCADGui as Gui
    filePath = WBAuxiliaries.workbenchFolderPath() + "\\Commands\\" + item.text()
    filePath = filePath.replace('\\', '/')
    if sys.version_info.major < 3:
        command = 'execfile("' + filePath + '")'
    else:
        # exec(compile(open(file).read(), file, 'exec'))
        command = 'exec(compile(open("' + filePath + '", encoding="utf-8").read(),"' + filePath + '", "exec"))'
    Gui.doCommand(command)


def filterList(listItems, txtFilter):
    for i in range(listItems.count()):
        txtItem = str(listItems.item(i).text())

        if not txtItem.startswith(txtFilter):
            listItems.item(i).setHidden(True)
        else:
            listItems.item(i).setHidden(False)


def CreateGui():
    mWindow = FreeCAD.Gui.getMainWindow()
    createDockWindows(mWindow)


if __name__ == "__main__":
    # execfile("C:\Users\heinrich\Desktop\FreeCAD18\Mod\!EngineeringBase\GuiTab.py")
    CreateGui()
