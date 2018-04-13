from direct.showbase.ShowBase import ShowBase
import scene


class Engine(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.map = scene.Scene(self)
        self.player = self.map.player

        self.disableMouse()
        self.camera.setPos(0, -64, 0)
        self.accept("arrow_left", self.key, ["a"])
        self.accept("arrow_right", self.key, ["d"])
        self.accept("arrow_up", self.key, ["w"])
        self.accept("arrow_down", self.key, ["s"])
        self.accept("space", self.key, ["eat"])

    def key(self, event):
        self.map.player.key(event)
        pass

g_engine = Engine()