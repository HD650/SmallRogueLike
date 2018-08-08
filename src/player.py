from database.action.action import *
from src import object

player = {
             "name": "player",
             "Ability": [MobileAbility],
             "texture": "player.png",
             "hp": 100,
             "mp": 100,
             "transparent": False,
             "collision": True,
         }


class Player(object.Object):
    def __init__(self):
        object.Object.__init__(self, player, None)

    def handle_key(self, event):
        pos = self["node"].getPos()
        if event is "w":
            pos.z += 1
        if event is "s":
            pos.z -= 1
        if event is "a":
            pos.x -= 1
        if event is "d":
            pos.x += 1

        do_ability(MobileAbility, self, pos.x, pos.z)
