import FreeCADGui, Part
from pivy.coin import *

class line:
    "this class will create a line after the user clicked 2 points on the screen"
    def __init__(self):
        self.view = FreeCADGui.ActiveDocument.ActiveView
        self.stack = []
        self.point = None

        # adding 2 callback functions
        self.callbackClick = self.view.addEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.click)
        self.callbackMove = self.view.addEventCallbackPivy(SoLocation2Event.getClassTypeId(),self.move)

    def move(self,event_cb):
        event = event_cb.getEvent()
        mousepos = event.getPosition()
        ctrl = event.wasCtrlDown()
        self.point = FreeCADGui.Snapper.snap(mousepos,active=ctrl)

    def click(self,event_cb):
        event = event_cb.getEvent()
        if event.getState() == SoMouseButtonEvent.DOWN:
            if self.point:
                self.stack.append(self.point)
            if len(self.stack) == 2:
                #l = Part.Line(self.stack[0],self.stack[1])
                #shape = l.toShape()
                #Part.show(shape)
                self.view.removeEventCallbackPivy(SoMouseButtonEvent.getClassTypeId(),self.callbackClick)
                self.view.removeEventCallbackPivy(SoLocation2Event.getClassTypeId(),self.callbackMove)
                FreeCADGui.Snapper.off()

line()