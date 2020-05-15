import FreeCAD
import FreeCADGui


class EBWorkbench (Workbench):

    MenuText = "Engineering Base"
    ToolTip = "Engineering Base workbench"
    #Icon = """paste here the contents of a 16x16 xpm icon"""

    def Initialize(self):
        #"This function is executed when FreeCAD starts"
        import EB_Commands, MeasureEdges # import here all the needed files that create your FreeCAD commands
        self.list = (["Clear_Console",
                    "Get_EB_Shape", 
                    "Get_EB_Shape_Step", 
                    "Add_EB_Shape_With_Shift",
                    "Add_EB_Shape_With_Shift_Step",
                    "Add_EB_Step_Assembly",
                    "Select_EB_Shape"]) # A list of command names created in the line above
        self.appendToolbar("EB Commands",self.list) # creates a new toolbar with your commands
        self.appendMenu("Engineering Base",self.list) # creates a new menu
        self.listAux =(["Get_DIN_Rail_TS35",
                        "Get_Terminal_Block",
                        "Get_GuiTab"])
        self.appendToolbar("EB Aux",self.listAux)
        # import Draft tools, icons
        try:
            import os,Draft_rc,DraftTools, DraftGui, Draft
            from DraftTools import translate
            FreeCADGui.addLanguagePath(":/translations")
            FreeCADGui.addIconPath(":/icons")
        except Exception as inst:
            print(inst)
            FreeCAD.Console.PrintError("Error: Initializing one or more of the Draft modules failed, Draft will not work as expected.\n")
        self.createList = ["Draft_Line","Draft_Wire","Draft_Circle","Draft_Ellipse",
                        "Draft_Polygon","Draft_Rectangle","Draft_Point"]
        self.appendToolbar("Create",self.createList)
        self.moveList =["Mover_For_Object", "Draft_Move","Draft_Rotate","Move_Piont_To_Point", "Rotate_Sel_Object_15"]
        self.appendToolbar("EB Move",self.moveList)
        self.visibilityList = ["Set_Transparancy", "Set_Display_Mode_Wire_Frame", 
                  "Set_Display_Mode_Flat_Lines", "Set_Visibility_True"]
        self.appendToolbar("EB Visibility",self.visibilityList)
        #self.appendMenu(["An existing Menu","My submenu"],self.list) # appends a submenu to an existing menu

    def Activated(self):
        #"This function is executed when the workbench is activated"
        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.Activated()
        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.show()
        return

    def Deactivated(self):
        #"This function is executed when the workbench is deactivated"
        import EB_Auxiliaries
        import subprocess
        fileDeletePYCfiles = EB_Auxiliaries.scriptDeletePYCfilesPath()
        subprocess.call("wscript.exe " + fileDeletePYCfiles)
        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.Deactivated()
        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.hide()
        return

    def ContextMenu(self, recipient):
        #"This is executed whenever the user right-clicks on screen"
        # "recipient" will be either "view" or "tree"
        self.appendContextMenu("EB commands",self.list) # add commands to the context menu

    def GetClassName(self): 
        # this function is mandatory if this is a full python workbench
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(EBWorkbench())