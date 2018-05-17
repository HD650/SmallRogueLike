from database.action.action import action_move
import object
from utils import *


class Player(object.Object):
    def __init__(self):
        object.Object.__init__(self, None, None)
        self.attributes["height"] = 1
        self.attributes["volume"] = 1
        self.attributes["value"] = 0
        self.attributes["texture"] = "player.png"
        self.attributes["node"] = None
        self.attributes["update"] = None
        self.attributes["speed"] = 5

        self.attributes["node"] = load_model(self.attributes["texture"])

    def handle_key(self, event):
        pos = self.attributes["node"].getPos()
        if event is "w":
            pos.z += 1
        if event is "s":
            pos.z -= 1
        if event is "a":
            pos.x -= 1
        if event is "d":
            pos.x += 1
        action_move(self, pos.x, pos.z)