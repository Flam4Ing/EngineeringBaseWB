import FreeCAD
import Part
from Utils.EB_Print import *

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


def GetConnectedEdges(someshape, selected_edge):
    #https: // forum.freecadweb.org / viewtopic.php?t = 30872
    connected_edges = []
    for edge in someshape.Edges:
        for vertex1 in edge.Vertexes:
            for vertex2 in selected_edge.Vertexes:
                if vertex1.isSame(vertex2):
                    connected_edges.append(edge)

