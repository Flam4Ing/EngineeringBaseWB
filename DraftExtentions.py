def Test():
    print("test")

import FreeCAD
import Part
import FreeCADGui
import DraftTools
import Draft
import clsDINRailTS35
import clsWiringDuct
from pivy import coin

class PlaceDeviceOnPoint(DraftTools.Creator):
    "this class will put shape after the user clicks a point on the screen"


    def Activated(self, shapeType = None):
        DraftTools.Creator.Activated(self)
        self.ShapeType = shapeType
        self.view = Draft.get3DView()
        self.stack = []
        rot = self.view.getCameraNode().getField("orientation").getValue()
        upv = DraftTools.Vector(rot.multVec(coin.SbVec3f(0,1,0)).getValue())
        DraftTools.plane.setup(self.view.getViewDirection().negative(), DraftTools.Vector(0,0,0), upv)
        self.point = None
        if self.ui:
            self.ui.pointUi()
            self.ui.continueCmd.show()
        # adding 2 callback functions
        self.callbackClick = self.view.addEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.click)
        self.callbackMove = self.view.addEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(),self.move)

    def move(self,event_cb):
        event = event_cb.getEvent()
        mousepos = event.getPosition().getValue()
        ctrl = event.wasCtrlDown()
        self.point = FreeCADGui.Snapper.snap(mousepos,active=ctrl)
        if self.ui:
            self.ui.displayPoint(self.point)

    def numericInput(self,numx,numy,numz):
        "called when a numeric value is entered on the toolbar"
        self.point = FreeCAD.Vector(numx,numy,numz)
        self.click()

    def click(self,event_cb=None):
        if event_cb:
            event = event_cb.getEvent()
            if event.getState() != coin.SoMouseButtonEvent.DOWN:
                return
        if self.point:
            self.stack.append(self.point)
            if len(self.stack) == 1:
                self.view.removeEventCallbackPivy(coin.SoMouseButtonEvent.getClassTypeId(),self.callbackClick)
                self.view.removeEventCallbackPivy(coin.SoLocation2Event.getClassTypeId(),self.callbackMove)
                # building commands
                if self.ShapeType == "Step":
                    import clsGetDeviceEB
                    sh = clsGetDeviceEB.GetEBDevice(True)
                    sh.Placement.Base = self.point
                if self.ShapeType == "Box":
                    import clsGetDeviceEB
                    sh = clsGetDeviceEB.GetEBDevice()
                    sh.Placement.Base = self.point
                if self.ShapeType == "TS35":
                    import clsDINRailTS35
                    sh = clsDINRailTS35.GetDINRailTS35()
                    sh.Placement.Base = self.point
                
                FreeCADGui.Snapper.off()
            self.finish()

    def finish(self,cont=False):
        "terminates the operation and restarts if needed"
        DraftTools.Creator.finish(self)
        if self.ui:
            if self.ui.continueMode:
                self.Activated()




class PlaceOnDraftGrid(DraftTools.Creator):
    "Place DINRail or wiring chanel on the Draft Grid"

    
    def Activated(self, shapeType = None):
        self.ShapeType = shapeType
        name = DraftTools.translate("draft","Rectangle")
        DraftTools.Creator.Activated(self,name)
        if self.ui:
            self.refpoint = None
            self.ui.pointUi(name)
            self.ui.extUi()
            self.call = self.view.addEventCallback("SoEvent",self.action)
            self.rect = DraftTools.rectangleTracker()
            DraftTools.msg(DraftTools.translate("draft", "Pick first point:")+"\n")

    def finish(self,closed=False,cont=False):
        "terminates the operation and closes the poly if asked"
        DraftTools.Creator.finish(self)
        if self.ui:
            self.rect.off()
            self.rect.finalize()
        if self.ui:
            if self.ui.continueMode:
                self.Activated()

    def createObject(self):
        "creates the final object in the current doc"
        FreeCADGui.addModule("Draft")
        pl = FreeCAD.Placement()
        p1 = self.node[0]
        p3 = self.node[-1]
        diagonal = p3.sub(p1)
        p2 = p1.add(DraftTools.DraftVecUtils.project(diagonal, DraftTools.plane.v))
        p4 = p1.add(DraftTools.DraftVecUtils.project(diagonal, DraftTools.plane.u))
        length = p4.sub(p1).Length
        height = p2.sub(p1).Length
        try:
            
            #Draw verical
            if height > length:
                length = height
                if p1.y < p3.y:
                    if p1.x < p3.x:
                        pl.Rotation = FreeCAD.Rotation(-90,0,0)
                        base = p2
                    else:
                        pl.Rotation = FreeCAD.Rotation(90,0,0)
                        base = p1
                    print("p1<p3")
                else:
                    if p1.x < p3.x:
                        pl.Rotation = FreeCAD.Rotation(-90,0,0)
                        base = p1
                    else:
                        pl.Rotation = FreeCAD.Rotation(90,0,0)
                        base = p2
            #Draw horisontal
            else:
                if p1.x < p4.x:
                    base = p1
                else:
                    base = p4
            
            #lineDirection =    Part.makeLine((p1.x, p1.y, p1.z), (p4.x, p4.y, p4.z))
            #Part.show(lineDirection)
            #plane_line1 =Part.LineSegment(p1, p2)
            #plane_line2 =Part.LineSegment(p2, p3)
            #plane_line3 =Part.LineSegment(p3, p4)
            #plane_line4 =Part.LineSegment(p4, p1)
            #plane_shap =Part.Shape([plane_line1, plane_line2, plane_line3, plane_line4])
            #plane_wire =Part.Wire(plane_shape.Edges)
            #plane_face =Part.Face(plane_wire)
            #Part.show(plane_face)
            pl.Base = base
            #pl.Rotation.Q = DraftTools.plane.getRotation().Rotation.Q
            if self.ShapeType == "TS35":
                self.CreateDINRail(length, pl)
            if self.ShapeType == "WD":
                self.CreateWiringDuct(length, pl)


                
        except:
            import traceback, sys 
            exc_tb = sys.exc_traceback
            print("Failure in line: " + str(traceback.tb_lineno(exc_tb)))
            print("Draft: error delaying commit")
        self.finish(cont=True)

    def action(self,arg):
        "scene event handler"
        if arg["Type"] == "SoKeyboardEvent":
            if arg["Key"] == "ESCAPE":
                self.finish()
        elif arg["Type"] == "SoLocation2Event": #mouse movement detection
            self.point,ctrlPoint,info = DraftTools.getPoint(self,arg,mobile=True,noTracker=True)
            self.rect.update(self.point)
            DraftTools.redraw3DView()
        elif arg["Type"] == "SoMouseButtonEvent":
            if (arg["State"] == "DOWN") and (arg["Button"] == "BUTTON1"):
                if (arg["Position"] == self.pos):
                    self.finish()
                else:
                    if (not self.node) and (not self.support):
                        DraftTools.getSupport(arg)
                        self.point,ctrlPoint,info = DraftTools.getPoint(self,arg,mobile=True,noTracker=True)
                    if self.point:
                        self.ui.redraw()
                        self.appendPoint(self.point)

    def numericInput(self,numx,numy,numz):
        "this function gets called by the toolbar when valid x, y, and z have been entered there"
        self.point = Vector(numx,numy,numz)
        self.appendPoint(self.point)

    def appendPoint(self,point):
        self.node.append(point)
        if (len(self.node) > 1):
            self.rect.update(point)
            self.createObject()
        else:
            DraftTools.msg(DraftTools.translate("draft", "Pick opposite point:")+"\n")
            self.ui.setRelative()
            self.rect.setorigin(point)
            self.rect.on()
            if self.planetrack:
                self.planetrack.set(point)

    def CreateDINRail(self,length,placement):
        r = clsDINRailTS35.GetDINRailTS35(length)
        r.Placement = placement
        FreeCAD.ActiveDocument.recompute()

    def CreateWiringDuct(self,length,placement):
        d = clsWiringDuct.GetWiringDuct(length)
        d.Placement = placement
        FreeCAD.ActiveDocument.recompute()

if __name__ == "__main__":
# execfile("C:\Users\heinrich\Desktop\FreeCAD18\Mod\!EngineeringBase\DraftExtentions.py")
    Test()
    PlaceOnDraftGrid().Activated("TS35")
