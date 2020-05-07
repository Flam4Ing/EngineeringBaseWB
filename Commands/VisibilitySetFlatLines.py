import WBAuxiliaries


def ToggleFlatLines():
    selObjects = WBAuxiliaries.GetSelectionWithSubObjects()
    if len(selObjects) != 0:
        for obj in selObjects:
            # print(obj.ViewObject.DisplayMode)
            if obj.ViewObject.DisplayMode == "Wireframe":
                obj.ViewObject.DisplayMode = "Flat Lines"


ToggleFlatLines()
