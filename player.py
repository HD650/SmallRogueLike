from database.action.action import action_move
import object


class Player(object.Object):
    def __init__(self):
        attributes = dict()
        attributes["height"] = 1
        attributes["volume"] = 1
        attributes["value"] = 0
        attributes["texture"] = "player.png"
        attributes["node"] = None
        attributes["update"] = None
        attributes["speed"] = 5
        object.Object.__init__(self, attributes, None)


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
