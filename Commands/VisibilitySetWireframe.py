import EB_Auxiliaries

def ToggleWireFrame():
    selObjects = EB_Auxiliaries.GetSelectionWithSubObjects()
    if len(selObjects) != 0:
        for obj in selObjects:
            #print(obj.ViewObject.DisplayMode)
            if obj.ViewObject.DisplayMode == "Flat Lines":
                obj.ViewObject.DisplayMode = "Wireframe"

ToggleWireFrame()