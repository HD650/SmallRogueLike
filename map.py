from utils import *


class Map:
    def __init__(self, engine,player):
        self.map = dict()
        self.tiles = list()
        self.objects = list()
        self.node = NodePath('map')
        self.node.reparentTo(engine.render)
        self.objects.append(player)
        self.objects[-1].reparentTo(self.node)
        for x in range(100):
            for y in range(100):
                self.tiles.append(loadObject("ship.png"))
                self.tiles[-1].reparentTo(self.node)
                self.tiles[-1].setPos(x, 0, y)
