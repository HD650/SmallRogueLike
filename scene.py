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
        # bitmap for collision and transparent
        self.tran_bitmap = None
        self.coll_bitmap = None
        # engine related render layer, all objects in this scene should be children of this node
        self.node = None
        # player in this scene
        self.player = None
        # all objects that contain conscious keyword
        self.conscious_objects = None
        self.width = None
        self.height = None
        # record the tiles in fov of player last turn, for fog of war optimize purpose
        self.fov_buffer = None

    def generate_mask(self):
        from engine import mask_z
        for x in range(100):
            for y in range(100):
                temp = object.Object(tile.tiles["fog_of_war"], self.node)
                temp["node"].setPos(x, mask_z, y)
                temp["node"].setColor(0, 0, 0, 1.0)
                self.mask[x][y] = temp

    def generate_tiles(self):
        # generate the tiles
        from engine import tiles_z
        # TODO the scene generator
        for x in range(100):
            for y in range(100):
                if random() > 0.8:
                    temp = object.Object(tile.tiles["stone_wall"], self.node)
                    temp["node"].setPos(x, tiles_z, y)
                else:
                    temp = object.Object(tile.tiles["grass_ground"], self.node)
                    temp["node"].setPos(x, tiles_z, y)
                self.map[x][y].append(temp)

    def generate_objects(self):
        from engine import object_z
        for i in range(20):
            temp = object.Object(monster.monsters["stone_dummy"], self.node)
            temp["node"].setPos(5*i, object_z, 5*i)
            self.map[5*i][5*i].append(temp)
            self.conscious_objects.append(temp)

    def generate_bitmap(self):
        # after this, we update bitmap when move, and only update location related to this movement, not whole
        for x in range(self.width):
            for y in range(self.height):
                self.tran_bitmap[x][y] = True
                self.coll_bitmap[x][y] = False
                for item in self.map[x][y]:
                    if "transparent" in item and not item["transparent"]:
                        self.tran_bitmap[x][y] = False
                    if "collision" in item and item["collision"]:
                        self.coll_bitmap[x][y] = True

    def update_bitmap(self, x, y):
        self.tran_bitmap[x][y] = True
        self.coll_bitmap[x][y] = False
        for item in self.map[x][y]:
            if "transparent" in item and not item["transparent"]:
                self.tran_bitmap[x][y] = False
            if "collision" in item and item["collision"]:
                self.coll_bitmap[x][y] = True

    def get_ready(self):
        # first and second dimension of self.map represents the location
        # final dimension is a list, contains all the object in this location
        # list is in order, eg tile is always the first one in list
        self.map = dict()
        self.conscious_objects = list()
        self.mask = dict()
        self.coll_bitmap = dict()
        self.tran_bitmap = dict()
        self.fov_buffer = list()
        self.width = 100
        self.height = 100
        for i in range(100):
            self.map[i] = dict()
            self.mask[i] = dict()
            self.coll_bitmap[i] = dict()
            self.tran_bitmap[i] = dict()
            for ii in range(100):
                self.map[i][ii] = list()

        # render this scene
        from engine import g_engine as engine
        self.node = NodePath('level')
        self.node.reparentTo(engine.render)

        # generate the ground or walls
        self.generate_tiles()
        # generate the fog of war (not init yet, wait until the player is spawned)
        self.generate_mask()
        # generate monsters, items etc...
        self.generate_objects()
        # generate the collision and transparent bit map according to all the objects generated above
        self.generate_bitmap()

    def add_player(self, player, x, y):
        from engine import player_z, g_engine as engine
        player["node"].setPos((x, player_z, y))
        player["node"].reparentTo(self.node)
        engine.camera.reparentTo(player["node"])
        self.map[player["node"].getPos().x][player["node"].getPos().z].append(player)
        self.player = player
        self.update_mask()

    def move_object(self, obj, ori_x, ori_y, new_x, new_y):
        if obj in self.map[ori_x][ori_y]:
            # the test function of action already check the availability of this movement, we don't need to check again
            self.map[ori_x][ori_y].remove(obj)
            self.update_bitmap(ori_x, ori_y)
            self.map[new_x][new_y].append(obj)
            self.update_bitmap(new_x, new_y)
            return True
        else:
            return False

    def remove_mask(self, x, y):
        # all tiles in our sight should be lit
        self.mask[x][y]["node"].setAlphaScale(0)
        # terrain we seen before will be record
        self.mask[x][y]["visited"] = True
        # objects in our sight should be revealed
        for obj in self.map[x][y][1:]:
            obj["node"].setAlphaScale(1.0)
        # record the tiles we watched
        self.fov_buffer.append((x, y))

    def update_mask(self):
        # if the tiles in our sight last turn now out of our sight, darken it
        for loc in self.fov_buffer:
            if self.mask[loc[0]][loc[1]]["visited"]:
                self.mask[loc[0]][loc[1]]["node"].setAlphaScale(0.5)
                # we can't see things in the shadow
                for obj in self.map[loc[0]][loc[1]][1:]:
                    obj["node"].setAlphaScale(0)
        # empty the buffer
        self.fov_buffer = list()
        # refresh the fov
        player_loc = self.player["node"].getPos()
        fieldOfView(int(player_loc.x), int(player_loc.z), self.width, self.height, 10, self.remove_mask,
                    test_tile_opaque)
