from database.object import tile
from panda3d.core import *
import object


class Scene:
    def __init__(self):
        # a 3d list to maintain objects in this scene
        self.map = None
        # engine related render layer, all objects in this scene should be children of this node
        self.node = None
        # player in this scene
        self.player = None

    def get_ready(self):
        # first and second dimension of self.map represents the location
        # final dimension is a list, contains all the object in this location
        # list is in order, eg tile is always the first one in list
        self.map = dict()
        for i in range(100):
            self.map[i] = dict()
            for ii in range(100):
                self.map[i][ii] = list()

        # render this scene
        from engine import g_engine as engine
        self.node = NodePath('level')
        self.node.reparentTo(engine.render)

        # TODO the scene generator
        for x in range(100):
            for y in range(100):
                temp = object.Object(tile.tiles["grass_ground"], self.node)
                temp.attributes["node"].setPos(x, 0, y)
                self.map[x][y].append(temp)

    def add_player(self, player, x, y):
        from engine import g_engine as engine
        player.attributes["node"].setPos((x, -1, y))
        player.attributes["node"].reparentTo(self.node)
        engine.camera.reparentTo(player.attributes["node"])
        self.map[player.attributes["node"].getPos().x][player.attributes["node"].getPos().z].append(player)
        self.player = player