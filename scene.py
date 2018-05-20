from database.object import tile
from database.object import monster
from panda3d.core import *
from database.action.test import test_tile_opaque
import object
from fov import fieldOfView

from random import random


class Scene:
    def __init__(self):
        # a 3d list to maintain objects in this scene
        self.map = None
        # mask to implement fog of war
        self.mask = None
        # engine related render layer, all objects in this scene should be children of this node
        self.node = None
        # player in this scene
        self.player = None
        # all objects that contain conscious keyword
        self.conscious_objects = None
        self.width = None
        self.height = None

    def generate_mask(self):
        from engine import mask_z
        for x in range(100):
            for y in range(100):
                temp = object.Object(tile.tiles["fog_of_war"], self.node)
                temp.attributes["node"].setPos(x, mask_z, y)
                temp.attributes["node"].setColor(0, 0, 0, 255)
                self.mask[x][y] = temp

    def get_ready(self):
        from engine import object_z, tiles_z
        # first and second dimension of self.map represents the location
        # final dimension is a list, contains all the object in this location
        # list is in order, eg tile is always the first one in list
        self.map = dict()
        self.conscious_objects = list()
        self.mask = dict()
        self.width = 100
        self.height = 100
        for i in range(100):
            self.map[i] = dict()
            self.mask[i] = dict()
            for ii in range(100):
                self.map[i][ii] = list()

        # render this scene
        from engine import g_engine as engine
        self.node = NodePath('level')
        self.node.reparentTo(engine.render)

        # TODO the scene generator
        for x in range(100):
            for y in range(100):
                if random() > 0.8:
                    temp = object.Object(tile.tiles["stone_ground"], self.node)
                    temp.attributes["node"].setPos(x, tiles_z, y)
                    temp.attributes["transparent"] = False
                else:
                    temp = object.Object(tile.tiles["grass_ground"], self.node)
                    temp.attributes["node"].setPos(x, tiles_z, y)
                self.map[x][y].append(temp)

        self.generate_mask()

        for i in range(10):
            temp = object.Object(monster.monsters["stone_dummy"], self.node)
            temp.attributes["node"].setPos(i*5, object_z, i*5)
            self.map[i*5][i*5].append(temp)
            self.conscious_objects.append(temp)

    def add_player(self, player, x, y):
        from engine import player_z, g_engine as engine
        player.attributes["node"].setPos((x, player_z, y))
        player.attributes["node"].reparentTo(self.node)
        engine.camera.reparentTo(player.attributes["node"])
        self.map[player.attributes["node"].getPos().x][player.attributes["node"].getPos().z].append(player)
        self.player = player
        self.update_mask()

    def remove_mask(self, x, y):
        self.mask[x][y].attributes["node"].setColor(0, 0, 0, 0)

    def update_mask(self):
        for x in range(self.width):
            for y in range(self.height):
                self.mask[x][y].attributes["node"].setColor(0, 0, 0, 255)
        player_loc = self.player.attributes["node"].getPos()
        fieldOfView(int(player_loc.x), int(player_loc.z), self.width, self.height, 15, self.remove_mask, test_tile_opaque)

