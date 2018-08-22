from database.action.action import *
from src import object

player = {
             "name": "player",
             "Ability": [MobileAbility, BaseCombatAbility],
             "texture": "player.png",
             "Hp": 100,
             "P_A": 10,
             "P_D": 5,
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
        if event is 'enter':
            return BaseCombatAbility
        if event is 'escape':
            return False

        # move ability is the only ability not handled by gui
        do_ability(MobileAbility, self, pos.x, pos.z)
       
        # if player move, go to next turn
        return True
