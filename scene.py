from database.object import tile
from player import Player
from panda3d.core import *
import object
from utils import *


class Scene:
    def __init__(self, engine):
        # first and second dimension of self.map represents the location
        # final dimension is a list, contains all the object in this location
        # list is in order, eg tile is always the first one in list
        self.map = dict()
        for i in range(100):
            self.map[i] = dict()
            for ii in range(100):
                self.map[i][ii] = list()

        self.node = NodePath('level')
        self.node.reparentTo(engine.render)

        self.player = Player(self.node)
        self.player.attributes["node"].setPos((0, -1, 0))
        engine.camera.reparentTo(self.player.attributes["node"])

        for x in range(100):
            for y in range(100):
                temp = object.Object(tile.tiles["grass_ground"], self.node)
                temp.attributes["node"].setPos(x, 0, y)
                self.map[x][y].append(temp)

        self.map[self.player.attributes["node"].getPos().x][self.player.attributes["node"].getPos().z].append(self.player)
