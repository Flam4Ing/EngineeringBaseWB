import FreeCADGui

class SelectionGate(object):
  def allow(self, doc, obj, sub):
    #if not obj.isDerivedFrom("Part::Feature"):
      #return False
    if not str(sub).startswith("Edge"):
      return False
    edge = getattr(obj.Shape, sub)
    if edge.isClosed():
      if isinstance(edge.Curve, Part.Circle):
        self.circle = edge
        return True
    return False


gate=SelectionGate()
FreeCADGui.Selection.addSelectionGate(gate)
#FreeCADGui.Selection.removeSelectionGate()