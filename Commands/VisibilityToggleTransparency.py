import FreeCADGui

def toggle_transparency_subtree(objs):
    def addsubobjs(obj,totoggleset):
        totoggle.add(obj)
        for subobj in obj.OutList:
            addsubobjs(subobj,totoggleset)

    import FreeCAD
    doc=FreeCADGui.ActiveDocument
    totoggle=set()
    for obj in objs:
        addsubobjs(obj,totoggle)
    checkinlistcomplete =False
    while not checkinlistcomplete:
        for obj in totoggle:
            if (obj not in objs) and (frozenset(obj.InList) - totoggle):
                try:
                    totoggle.toggle(obj)
                    break
                except:
                    FreeCAD.Console.PrintWarning('totoggle not allowed\n')
        else:
            checkinlistcomplete = True
    for obj in totoggle:
        #if 'App::Part' not in obj.TypeId and 'Part::Feature' in obj.TypeId:
        if 'App::Part' not in obj.TypeId and 'Part' in obj.TypeId:
            #if obj.Visibility==True:
            if doc.getObject(obj.Name).Transparency == 0:
                #obj.Document.getObject(obj.Name).Visibility=False
                doc.getObject(obj.Name).Transparency = 70
            else:
                doc.getObject(obj.Name).Transparency = 0
##
class ksuToolsTransparencyToggle:
    "ksu tools Transparency Toggle"
 
    def GetResources(self):
        return {'Pixmap'  : os.path.join( ksuWB_icons_path , 'transparency_toggle.svg') , # the name of a svg file available in the resources
                     'MenuText': "ksu Transparency Toggle" ,
                     'ToolTip' : "Selection Transparency Toggle"}
 
    def IsActive(self):
        return True
 
    def Activated(self):
        # do something here...
        if FreeCADGui.Selection.getSelection():
            sel=FreeCADGui.Selection.getSelection()
            doc=FreeCADGui.ActiveDocument
            for obj in sel:
                if not ("App::Part" in obj.TypeId or "App::DocumentObjectGroup" in obj.TypeId):
                    if doc.getObject(obj.Name).Transparency == 0:
                        doc.getObject(obj.Name).Transparency = 70
                    else:
                        doc.getObject(obj.Name).Transparency = 0
                else:
                    toggle_transparency_subtree(FreeCADGui.Selection.getSelection())
        else:
            #FreeCAD.Console.PrintError("Select elements from dxf imported file\n")
            reply = QtGui.QMessageBox.information(None,"Warning", "Select one or more object(s) to change its transparency!")
            FreeCAD.Console.PrintWarning("Select one or more object(s) to change its transparency!\n")             

#FreeCADGui.addCommand('ksuToolsTransparencyToggle',ksuToolsTransparencyToggle())

tg = ksuToolsTransparencyToggle().Activated()