import FreeCAD
import FreeCADGui
import Draft
import Part
import EB_Auxiliaries


class Get_MeassureEdges():
    def GetResources(self):
        return {'Pixmap': EB_Auxiliaries.workbenchFolderPath() + "\Icons\Visibility_Transparency.svg",
                'MenuText': "Meassure Edges"}

    def Activated(self):
        """Do something here"""
        self.Messen()
        return

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Messen(self):
        sel = FreeCADGui.Selection.getSelectionEx()
        if len(sel) == 1:

            if "Edge" in sel[0].SubElementNames[0]:
                edge = sel[0].SubObjects[0]
                if isinstance(edge.Curve, Part.Circle):
                    radius = edge.Curve.Radius
                    diametr = radius*2
                    EB_Auxiliaries.MsgDialog("Radius: " + str(radius) + "mm" + "\nDiametr: " + str(diametr) + "mm")
                if isinstance(edge.Curve, (Part.LineSegment, Part.Line)):
                    Start = edge.Vertexes[0].Point
                    End = edge.Vertexes[-1].Point
                    length = Start.sub(End).Length
                    EB_Auxiliaries.MsgDialog("Length: " + str(length) + "mm")

FreeCADGui.addCommand('Get_MeassureEdges', Get_MeassureEdges())