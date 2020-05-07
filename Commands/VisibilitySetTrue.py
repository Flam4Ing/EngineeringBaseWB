import WBAuxiliaries

def VisibilitySetTrue():
    selObjects = WBAuxiliaries.GetSelectionWithSubObjects()
    if len(selObjects) != 0:
        for obj in selObjects:
            #print(obj.ViewObject.Visibility)
            if "Visibility" in dir(obj.ViewObject):
                if not obj.TypeId == 'App::Origin':
                    obj.ViewObject.Visibility = True

VisibilitySetTrue()