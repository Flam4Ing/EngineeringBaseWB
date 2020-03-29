import  FreeCAD
import  FreeCADGui

def say(msg):
    print(msg)

def cb(point):
    if point:
        print("got a 3D point: ", point)


def Move():
    global initial_placement, last_selection
    global objs, objs_plc

    # get_ALGposition()
    # selection = [s for s in FreeCADGui.Selection.getSelectionEx() if s.Document == FreeCAD.ActiveDocument]
    selection = FreeCADGui.Selection.getSelectionEx()
    if len(selection) == 1:
        # if FreeCAD.ActiveDocument is not None:
        #     FreeCAD.ActiveDocument.openTransaction('Moving')
        objs = []
        last_selection = selection
        say('Move 1')
        p = selection[0].Object.Placement.Base
        selection[0].Object.Placement.Base = p
        PartMover(FreeCADGui.activeDocument().activeView(), selection[0].Object)
        say('starting ' + str(initial_placement))
    else:
        # PartMoverSelectionObserver()
        pass


class PartMover:
    global initial_placement, final_placement

    def __init__(self, view, obj):
        global initial_placement
        self.obj = obj
        self.initialPosition = self.obj.Placement.Base
        initial_placement = self.initialPosition
        say('init ' + str(initial_placement))
        obj.Placement.Base = self.initialPosition
        self.copiedObject = False
        self.view = view
        self.callbackMove = self.view.addEventCallback("SoLocation2Event", self.moveMouse)
        self.callbackClick = self.view.addEventCallback("SoMouseButtonEvent", self.clickMouse)
        self.callbackKey = self.view.addEventCallback("SoKeyboardEvent", self.KeyboardEvent)

    def moveMouse(self, info):
        newPos = self.view.getPoint(*info['Position'])
        p = info['Position']
        # print(str(info))
        self.obj.ViewObject.DisplayMode = "Wireframe"
        self.sPoint = FreeCADGui.Snapper.snap(p)
        self.obj.Placement.Base = newPos

    def removeCallbacks(self):
        self.view.removeEventCallback("SoLocation2Event", self.callbackMove)
        self.view.removeEventCallback("SoMouseButtonEvent", self.callbackClick)
        self.view.removeEventCallback("SoKeyboardEvent", self.callbackKey)
        FreeCADGui.Snapper.off()

    def clickMouse(self, info):
        global initial_placement
        # debugPrint(4, 'clickMouse info %s' % str(info))
        if info['Button'] == 'BUTTON1' and info['State'] == 'DOWN':
            if not info['ShiftDown'] and not info['CtrlDown']:
                say('releasing obj')
                _recompute = True
                if _recompute:
                    FreeCAD.ActiveDocument.recompute()
                # sayw('releasing\ninitial p: '+ str( initial_placement ))
                say('final p: ' + str(self.obj.Placement.Base))
                final_placement = self.obj.Placement.Base
                self.obj.Placement.Base = self.sPoint
                self.removeCallbacks()
            elif info['ShiftDown']:  # copy object
                pass
            elif info['CtrlDown']:
                pass

    def KeyboardEvent(self, info):
        # debugPrint(4, 'KeyboardEvent info %s' % str(info))
        if info['State'] == 'UP' and info['Key'] == 'ESCAPE':
            if not self.copiedObject:
                self.obj.Placement.Base = self.initialPosition
            else:
                FreeCAD.ActiveDocument.removeObject(self.obj.Name)
            self.removeCallbacks()


# class PartMoverSelectionObserver:
#     def __init__(self):
#         global initial_placement
#
#         FreeCADGui.Selection.addObserver(self)
#         FreeCADGui.Selection.removeSelectionGate()
#         if FreeCAD.ActiveDocument is not None:
#             FreeCAD.ActiveDocument.openTransaction('Moving 2')
#         if len(FreeCADGui.Selection.getSelection()) > 0:
#             p = FreeCADGui.Selection.getSelection()[0].Placement.Base
#             FreeCADGui.Selection.getSelection()[0].Placement.Base = p
#
#     def addSelection(self, docName, objName, sub, pnt):
#         # debugPrint(4,'addSelection: docName,objName,sub = %s,%s,%s' % (docName, objName, sub))
#         FreeCADGui.Selection.removeObserver(self)
#         obj = FreeCAD.ActiveDocument.getObject(objName)
#         view = FreeCADGui.activeDocument().activeView()
#         PartMover(view, obj)

# class MovePartCommand:
#     say('Move')
#     def Activated(self):
#         selection = [s for s in FreeCADGui.Selection.getSelectionEx() if s.Document == FreeCAD.ActiveDocument ]
#         if len(selection) == 1:
#             say('Move2')
#             PartMover( FreeCADGui.activeDocument().activeView(), selection[0].Object )
#         else:
#             PartMoverSelectionObserver()

# FreeCADGui.addCommand('assembly2_movePart', MovePartCommand())




Move()
