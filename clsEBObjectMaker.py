import WBAuxiliaries
import FreeCAD
import Part
import sys


def GetEBObjectMaker(DeviceType="EBDevice"):
    d = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", DeviceType)
    d.addProperty("App::PropertyString", "ADevice", "Engineering Base Information", "Device")
    d.addProperty("App::PropertyString", "BMK", "Engineering Base Information", "Device name")
    d.addProperty("App::PropertyVector", "BMKpos", "Engineering Base Information", "BMK position")
    d.addProperty("App::PropertyInteger", "BMKrot", "Engineering Base Information", "BMK rotation")
    d.addProperty("App::PropertyInteger", "BMKsize", "Engineering Base Information", "BMK size").BMKsize = 20
    d.addProperty("App::PropertyString", "STEPfile", "Engineering Base Information", "Path to STEP file")
    d.addProperty("App::PropertyString", "OID", "Engineering Base Information", "ID Nummer")
    d.addProperty("Part::PropertyPartShape", "EBShape", "Engineering Base Information", "EB Shape")
    d.addProperty("Part::PropertyPartShape", "PositionLine", "Engineering Base Information", "Position line")
    return d


def GetTextObj(BMK="Test", BMKsize=20):
    '''"Print a short message when doing a recomputation, this method is mandatory" '''
    txtString = BMK
    FontFile = WBAuxiliaries.fontFilePath()
    ff8 = FontFile.encode('utf8')
    Size = BMKsize
    Tracking = 0
    if sys.version_info.major < 3:
        CharList = Part.makeWireString(txtString, ff8, Size, Tracking)
    else:
        CharList = Part.makeWireString(txtString, FontFile, Size, Tracking)
    if len(CharList) == 0:
        print("ShapeString: string has no wires\n")
        return
    SSChars = []

    # test a simple letter to know if we have a sticky font or not
    sticky = False
    if sys.version_info.major < 3:
        testWire = Part.makeWireString("L", ff8, Size, Tracking)[0][0]
    else:
        testWire = Part.makeWireString("L", FontFile, Size, Tracking)[0][0]
    if testWire.isClosed:
        try:
            testFace = Part.Face(testWire)
        except Part.OCCError:
            sticky = True
        else:
            if not testFace.isValid():
                sticky = True
    else:
        sticky = True

    for char in CharList:
        if sticky:
            for CWire in char:
                SSChars.append(CWire)
        else:
            CharFaces = []
            for CWire in char:
                f = Part.Face(CWire)
                if f:
                    CharFaces.append(f)
            if CharFaces:
                s = makeFaces(char)
                SSChars.append(s)
    textObj = Part.Compound(SSChars)
    return textObj


def makeFaces(wireChar):
    compFaces = []
    allEdges = []
    wirelist = sorted(wireChar, key=(lambda shape: shape.BoundBox.DiagonalLength), reverse=True)
    fixedwire = []
    for w in wirelist:
        compEdges = Part.Compound(w.Edges)
        compEdges = compEdges.connectEdgesToWires()
        fixedwire.append(compEdges.Wires[0])
    wirelist = fixedwire
    sep_wirelist = []
    while len(wirelist) > 0:
        wire2Face = [wirelist[0]]
        face = Part.Face(wirelist[0])
        for w in wirelist[1:]:
            p = w.Vertexes[0].Point
            u, v = face.Surface.parameter(p)
            if face.isPartOfDomain(u, v):
                f = Part.Face(w)
                if face.Orientation == f.Orientation:
                    if f.Surface.Axis * face.Surface.Axis < 0:
                        w.reverse()
                else:
                    if f.Surface.Axis * face.Surface.Axis > 0:
                        w.reverse()
                wire2Face.append(w)
            else:
                sep_wirelist.append(w)
        wirelist = sep_wirelist
        sep_wirelist = []
        face = Part.Face(wire2Face)
        face.validate()
        if face.Surface.Axis.z < 0.0:
            face.reverse()
        compFaces.append(face)
    ret = Part.Compound(compFaces)
    return ret
