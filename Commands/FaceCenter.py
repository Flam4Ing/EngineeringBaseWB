import FreeCAD
import FreeCADGui
import Draft


def objectRealPlacement3D(obj):  # search the real Placement
    try:
        objectPlacement = obj.Shape.Placement
        objectPlacementBase = FreeCAD.Vector(objectPlacement.Base)

        ####
        objectWorkCenter = objectPlacementBase
        ####

        if hasattr(obj, "getGlobalPlacement"):
            globalPlacement = obj.getGlobalPlacement()
            globalPlacementBase = FreeCAD.Vector(globalPlacement.Base)
            ####
            objectRealPlacement3D = globalPlacementBase.sub(objectWorkCenter)  # mode=0 adapte pour BBox + Centerpoints
            ####
        else:
            objectRealPlacement3D = objectWorkCenter

        return objectRealPlacement3D
    except Exception:
        return FreeCAD.Vector(0.0, 0.0, 0.0)

def PointOnCenterFace():
    if len(FreeCADGui.Selection.getSelection()) > 0:
        sh = FreeCADGui.Selection.getSelection()[0]
        SubElement = FreeCADGui.Selection.getSelectionEx()[0]  # "getSelectionEx" Used for selecting subobjects
        selectedFace = SubElement.SubObjects[0]  # seletion of the first element
        if str(SubElement.SubElementNames[0]).startswith("Face"):
            oripl_X = selectedFace.CenterOfMass.x
            oripl_Y = selectedFace.CenterOfMass.y
            oripl_Z = selectedFace.CenterOfMass.z

            placementOrigine = objectRealPlacement3D(sh)
            oripl_X += placementOrigine[0]
            oripl_Y += placementOrigine[1]
            oripl_Z += placementOrigine[2]
            Draft.makePoint(oripl_X, oripl_Y, oripl_Z)
PointOnCenterFace()