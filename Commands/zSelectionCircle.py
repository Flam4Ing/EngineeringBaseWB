import FreeCADGui

def Test():
    TOL = 0.0001 # for checking curvature
    selection = FreeCADGui.Selection.getSelectionEx()
    for o in selection:
        # note, shouldn't need to check HasSubObjects, as if 
        #there are no SubObjects this for loop just won't execute
        for obj in o.SubObjects:
            #if len(obj.Edges) == 1 and abs(obj.Edges[0].Curve.curvature(0) - obj.Edges[0].Curve.curvature(1)) < TOL:
                    # note: we check the difference in curvature rather than
                    # equality due to floating point rounding errors
                print("this is most likely a circle")


def SearchCircles():
    TOL = 0.0001 # for checking curvature
    sel = FreeCADGui.Selection.getSelection()[0]
    for edge in sel.Shape.Edges:
            #if abs(edge.Curve.curvature(0) - edge.Curve.curvature(1)) < TOL:
            if edge.isClosed():
                    # note: we check the difference in curvature rather than
                    # equality due to floating point rounding errors
                print("this is most likely a circle")
                print (str(type(edge.Curve)))
                print (edge.Length)
SearchCircles()