import WBAuxiliaries

def ToggleWireFrame():
    selObjects = WBAuxiliaries.GetSelectionWithSubObjects()
    if len(selObjects) != 0:
        for obj in selObjects:
            #print(obj.ViewObject.DisplayMode)
            if obj.ViewObject.DisplayMode == "Flat Lines":
                obj.ViewObject.DisplayMode = "Wireframe"

ToggleWireFrame()