import FreeCAD
import FreeCADGui

class SelectionGate(object):
  def allow(self, doc, obj, sub):
    if not obj.isDerivedFrom("Part::Feature"):
      return False
    if str(sub).startswith("Vertex"):
      return True
    return False

#gate=SelectionGate()
#FreeCADGui.Selection.addSelectionGate(gate)
#FreeCADGui.Selection.removeSelectionGate()


def V2V():
    MouseSel = FreeCADGui.Selection.getSelectionEx()
    ObjA_Name = MouseSel[0].ObjectName
    ObjB_Name = MouseSel[1].ObjectName
    PointA = MouseSel[0].SubObjects[0].Point
    PointB = MouseSel[1].SubObjects[0].Point
    Vector = PointB - PointA
    Pos0 = FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Base
    Rot0 = FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement.Rotation
    #Rot0 = App.ActiveDocument.getObject(ObjB_Name).Placement.Rotation
    MVector = Pos0 + Vector
    FreeCAD.ActiveDocument.getObject(ObjA_Name).Placement = FreeCAD.Placement(MVector, Rot0)

V2V()