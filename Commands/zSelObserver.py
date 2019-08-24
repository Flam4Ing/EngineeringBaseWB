class SelObserver:
    def setPreselection(self,doc,obj,sub):                # Preselection object
        App.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name

    def addSelection(self,doc,obj,sub,pnt):               # Selection object
        App.Console.PrintMessage("addSelection"+ "\n")
        App.Console.PrintMessage(str(doc)+ "\n")          # Name of the document
        App.Console.PrintMessage(str(obj)+ "\n")          # Name of the object
        App.Console.PrintMessage(str(sub)+ "\n")          # The part of the object name
        App.Console.PrintMessage(str(pnt)+ "\n")          # Coordinates of the object
        App.Console.PrintMessage("______"+ "\n")

    def removeSelection(self,doc,obj,sub):                # Delete the selected object
        App.Console.PrintMessage("removeSelection"+ "\n")

    def setSelection(self,doc):                           # Selection in ComboView
        App.Console.PrintMessage("setSelection"+ "\n")

    def clearSelection(self,doc):                         # If click on the screen, clear the selection
        App.Console.PrintMessage("clearSelection"+ "\n")  # If click on another object, clear the previous object
s =SelObserver()
FreeCADGui.Selection.addObserver(s)
#FreeCADGui.Selection.removeObserver(s)