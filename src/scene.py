from random import random

from src import object
from src.fov import fieldOfView
from panda3d.core import NodePath

from database.action.test import test_tile_opaque
from database.object import monster
from database.object import tile


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

    def generate_mask(self):
        from src.engine import mask_z
        for x in range(100):
            for y in range(100):
                temp = object.Object(tile.tiles["fog_of_war"], self.node)
                temp["node"].setPos(x, mask_z, y)
                temp["node"].setColor(0, 0, 0, 1.0)
                self.mask[x][y] = temp

    def generate_tiles(self):
        # generate the tiles
        from src.engine import tiles_z
        # TODO the scene generator
        for x in range(100):
            for y in range(100):
                if random() > 0.8:
                    temp = object.Object(tile.tiles["stone_wall"], self.node)
                else:
                    temp = object.Object(tile.tiles["grass_ground"], self.node)
                self.add_object(temp, x, y, tiles_z)

    def generate_objects(self):
        from src.engine import object_z
        for i in range(20):
            temp = object.Object(monster.monsters["stone_dummy"], self.node)
            self.add_object(temp, i*5, i*5, object_z)
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
        from src.engine import g_engine as engine
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

    def add_object(self, obj, x, y, z):
        from src.engine import object_z
        # util method to add a object in scene since object influence al lot meta data in scene
        # if the obj has no model, addition failed
        if "node" not in obj:
            return False
        else:
            # update bitmap
            if "transparent" in obj and not obj["transparent"]:
                self.tran_bitmap[x][y] = False
            if "collision" in obj and obj["collision"]:
                self.coll_bitmap[x][y] = True
            if z is None:
                z = object_z
            obj["node"].setPos(x, z, y)
            # add to the map data structure
            self.map[x][y].append(obj)

    def remove_object(self, obj):
        if "node" not in obj:
            return False
        else:
            pos = obj["node"].getPos()
            self.map[pos.x][pos.z].remove(obj)
            obj["node"].removeNode()
            if "transparent" in obj or "collision" in obj:
                self.update_bitmap(pos.x, pos.z)
        if obj in self.conscious_objects:
            self.conscious_objects.remove(obj) 

    def add_player(self, player, x, y):
        from src.engine import player_z, g_engine as engine
        player["node"].reparentTo(self.node)
        engine.camera.reparentTo(player["node"])
        self.add_object(player, x, y, player_z)
        self.update_mask()

    def get_object(self, x, y):
        return self.map[x][y]

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
        for obj in self.map[x][y][1:]:
            obj["node"].setAlphaScale(1.0)
        # terrain we seen before will be record
        self.mask[x][y]["visited"] = True

    def update_mask(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.mask[x][y]["visited"]:
                    self.mask[x][y]["node"].setAlphaScale(0.5)
                    # we can't see things in the shadow
                    for obj in self.map[x][y][1:]:
                        obj["node"].setAlphaScale(0)
        from src.engine import g_engine as engine
        # refresh the fov
        player_loc = engine.player["node"].getPos()
        fieldOfView(int(player_loc.x), int(player_loc.z), self.width, self.height, 10, self.remove_mask,
                    test_tile_opaque)

    # update function called preturn
    def turn_update(self):
        print("Pre turn update")
        # update all objects
        for x in range(self.width):
            for y in range(self.height):
                for obj in self.map[x][y]:
                    obj.turn_update()
        # update all abilities AFTER all object finished update
        # here, passive abilities will try to interact with surrounding objects
        for x in range(self.width):
            for y in range(self.height):
                for obj in self.map[x][y]:
                    if "Ability" in obj:
                        for ab in obj["Ability"]:
                            obj[ab].turn_update()
        
        from src.engine import g_engine as engine
        # if we are not control player now, share the fov of the object we are controlling now
        if engine.player is not engine.now_control:
            player_loc = engine.now_control["node"].getPos()
            fieldOfView(int(player_loc.x), int(player_loc.z), self.width, self.height, 10, self.remove_mask,
                        test_tile_opaque)
