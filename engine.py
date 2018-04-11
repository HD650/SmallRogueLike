from direct.showbase.ShowBase import ShowBase
from map import Map
from player import Player


class Enginee(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.player=Player()
        self.map = Map(self,self.player.node)

        self.disableMouse()
        self.camera.setPos(0, -64, 0)
        self.accept("arrow_left", self.key,["a"])
        self.accept("arrow_left-up", self.key,[""])
        self.accept("arrow_right", self.key,["d"])
        self.accept("arrow_right-up", self.key,[""])
        self.accept("arrow_up", self.key,["w"])
        self.accept("arrow_down", self.key,["s"])
        self.accept("space", self.key,[""])

    def key(self,event):
        self.player.key(event)
        pass


demo = Enginee()
demo.run()
