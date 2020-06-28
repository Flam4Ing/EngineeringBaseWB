import FreeCAD
import ImportGui
import Part

def GetSingleShapeFromSTEP(file_path):
    doc = FreeCAD.ActiveDocument
    current_instances = set(doc.findObjects())
    ImportGui.insert(file_path, doc.Name)
    new_instances = list(set(doc.findObjects()) - current_instances)
    if not len(new_instances)== 1:
        DeleteObjects(doc, new_instances)
        return
    obj = new_instances[0]
    shape = Part.makeCompound(obj.Shape)
    newObj = doc.addObject("Part::Feature", "Test")
    newObj.Shape = obj.Shape.copy()
    newObj.ViewObject.ShapeColor = obj.ViewObject.ShapeColor
    newObj.ViewObject.DiffuseColor = obj.ViewObject.DiffuseColor
    doc.removeObject(obj.Name)

def DeleteObjects(doc, objects):
    for s in objects:
        try:
            doc.removeObject(s.Name)
        except:
            pass

def GetShapeFromSTEP(file_path):

    doc = FreeCAD.ActiveDocument
    current_instances = set(doc.findObjects())
    ImportGui.insert(file_path, doc.Name)
    new_instances = set(doc.findObjects()) - current_instances
    shapes = list(new_instances)
    sh = []
    cols = []
    areas = []

    for s in shapes:
        # print(s.TypeId)

        if hasattr(s, "Shape"):
            if hasattr(s.ViewObject, "DiffuseColor"):
                col = list(zip(s.Shape.Faces, s.ViewObject.DiffuseColor))
                print(len(s.Shape.Faces))
                print(len(s.ViewObject.DiffuseColor))
                print(s.ViewObject.DiffuseColor)
                print(len(col))
                cols.append(col)
                # print(s.ViewObject.DiffuseColor)
                sh.append(s.Shape)


    for c in cols:
        for faceshape, colortuple in c:
            areas.append((faceshape.Area, colortuple))





    # for s in shapes:
    #     try:
    #         doc.removeObject(s.Name)
    #     except:
    #         pass
    shape = Part.makeCompound(sh)
    # print(len(shape.Faces))
    # print(len(areas))
    Part.show(shape)


# GetShapeFromSTEP("C:\\Users\\Andrej\\Downloads\\STEP-2.14\\9666.926(2).stp")
# GetShapeFromSTEP("C:\\Users\Andrej\\Desktop\\Telemecanique\\New folder\\xb4_bd33-.stp")
GetSingleShapeFromSTEP("C:\\Users\Andrej\\Desktop\\Telemecanique\\New folder\\aaa.stp")