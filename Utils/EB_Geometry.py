import FreeCAD
import Part
from Utils.EB_Print import *


#------------------------------------------------------------------------------
def getObjectFaceFromName( obj, faceName ):
    assert faceName.startswith('Face')
    ind = int( faceName[4:]) -1
    return obj.Shape.Faces[ind]
#------------------------------------------------------------------------------
def getObjectEdgeFromName( obj, name ):
    assert name.startswith('Edge')
    ind = int( name[4:]) -1
    return obj.Shape.Edges[ind]
#------------------------------------------------------------------------------
def getObjectVertexFromName( obj, name ):
    assert name.startswith('Vertex')
    ind = int( name[6:]) -1
    return obj.Shape.Vertexes[ind]
#------------------------------------------------------------------------------
def centerLinePoint(edge, info=0):
    """ Return the center point of the Line.
    """
    # Vector_A=edge.valueAt( 0.0 )
    Vector_A = edge.Vertexes[0].Point
    if info != 0:
        print_point(Vector_A, "Origin of line selected is: ")
    # Vector_B=edge.valueAt( edge.Length )
    Vector_B = edge.Vertexes[-1].Point
    if info != 0:
        print_point(Vector_B, "End of line selected is: ")
    Vector_MidPoint = Vector_B + Vector_A
    center = Vector_MidPoint.multiply(0.5)
    if info != 0:
        print_point(center, "Center of line selected is: ")
    return center

#------------------------------------------------------------------------------
def edgeToVector(edge):
    """ Return a vector from an edge or a Part.line.
    """
    if isinstance(edge, Part.Shape):
        return edge.Vertexes[-1].Point.sub(edge.Vertexes[0].Point)
    elif isinstance(edge, Part.Line):
        return edge.EndPoint.sub(edge.StartPoint)
    else:
        print_msg("Error in edgeToVector(edge): not a good type of input" + str(type(edge)))
        return None

#------------------------------------------------------------------------------
def colinearEdges(edge1, edge2, info=0, tolerance=1e-12):
    """ Return true if 2 edges are colinear.
    """
    if not isinstance(edge1.Curve, Part.Line):
        if info != 0:
            print_msg("colinearEdges: edge1 not instance of Part.Line !")
        return False
    if not isinstance(edge2.Curve, Part.Line):
        if info != 0:
            print_msg("colinearEdges: edge2 not instance of Part.Line !")
        return False
    A = edgeToVector(edge1)
    B = FreeCAD.Base.Vector(0, 0, 0)
    C = edgeToVector(edge2)
    return colinearVectors(A, B, C, info=info, tolerance=tolerance)

#------------------------------------------------------------------------------
def colinearVectors(A, B, C, info=0, tolerance=1e-12):
    """ Return true if the 3 points are aligned.
    """
    Vector_1 = B - A
    Vector_2 = C - B
    if info != 0:
        print_point(Vector_1, msg="Vector_1: ")
        print_point(Vector_2, msg="Vector_2: ")
    Vector_3 = Vector_1.cross(Vector_2)
    if info != 0:
        print_point(Vector_3, msg="Vector_1.cross(Vector_2): ")

    if abs(Vector_3.x) <= tolerance and abs(Vector_3.y) <= tolerance and abs(Vector_3.z) <= tolerance:
        if info != 0:
            print_msg("Colinear Vectors !")
        return True
    else:
        if info != 0:
            print_msg("NOT Colinear Vectors !")
        return False
    return

#------------------------------------------------------------------------------
def angleBetween(e1, e2):
    """ Return the angle (in degrees) between 2 edges.
    """
    if isinstance(e1, Part.Edge) and isinstance(e2, Part.Edge):
        # Create the Vector for first edge
        v1 = e1.Vertexes[-1].Point
        v2 = e1.Vertexes[0].Point
        ve1 = v1.sub(v2)
        # Create the Vector for second edge
        v3 = e2.Vertexes[-1].Point
        v4 = e2.Vertexes[0].Point
        ve2 = v3.sub(v4)
    elif isinstance(e1, FreeCAD.Vector) and isinstance(e2, FreeCAD.Base.Vector):
        ve1 = e1
        ve2 = e2
    elif isinstance(e1, Part.Edge) and isinstance(e2, FreeCAD.Base.Vector):
        v1 = e1.Vertexes[-1].Point
        v2 = e1.Vertexes[0].Point
        ve1 = v1.sub(v2)
        ve2 = e2
    elif isinstance(e1, FreeCAD.Base.Vector) and isinstance(e2, Part.Edge):
        ve1 = e1
        v3 = e2.Vertexes[-1].Point
        v4 = e2.Vertexes[0].Point
        ve2 = v3.sub(v4)
    else:
        return

    angle = ve1.getAngle(ve2)
    import math
    return math.degrees(angle), angle

#------------------------------------------------------------------------------
def GetConnectedEdges(someshape, selected_edge):
    #https: // forum.freecadweb.org / viewtopic.php?t = 30872
    connected_edges = []
    for edge in someshape.Edges:
        for vertex1 in edge.Vertexes:
            for vertex2 in selected_edge.Vertexes:
                if vertex1.isSame(vertex2):
                    connected_edges.append(edge)



#------------------------------------------------------------------------------
def FindEdgeInObject(anEdge,inObject):
    for e in inObject.Shape.Edges:
        if e.Vertexes[0].Point == anEdge.Vertexes[0].Point:
               if e.Vertexes[-1].Point == anEdge.Vertexes[-1].Point:
                   return inObject.Shape.Edges.index(e) # we return the index of the edge in the edges list
    return None

#------------------------------------------------------------------------------
def SetFaceColour(obj, colour, facesBYareas, tolerance=1):
    numfaces = len(obj.Shape.Faces)
    """1 = 255
    color numer 10 = (1/255) * 10
    color numer 75 = (1/255) * 75"""
    # glb = (1.0, 1.0, 0.0)  # yellow
    # grn = (0., 1., 0.)  # green

    # colors = [rgb for i in range(numfaces)]
    defaultColour = obj.ViewObject.DiffuseColor[0]
    colors = []
    for i in obj.Shape.Faces:
        col = defaultColour
        for f in facesBYareas:
            if i.Area > f - tolerance and i.Area < f + tolerance:
                col = colour
                break

        colors.append(col)

    obj.ViewObject.DiffuseColor = colors