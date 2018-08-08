# conscious are keywords decorate objects
# with a conscious keyword, an object have their own will to move or act

from database.action.action import *


def chase_player(operator):
    from src.engine import g_engine as engine
    loc_now = operator["node"].getPos()
    loc_ply = engine.now_control["node"].getPos()
    direction = loc_ply - loc_now
    if abs(direction.x) <= 1 and abs(direction.z) <= 1:
        if operator[BaseCombatAbility].prerequisites():
            operator[BaseCombatAbility].perform([engine.now_control])
            return True
    
    direction.normalize()
    if direction.x > 0:
        loc_now.x += 1
    elif direction.x < 0:
        loc_now.x -= 1

    if direction.z > 0:
        loc_now.z += 1
    elif direction.z < 0:
        loc_now.z -= 1

    do_ability(MobileAbility, operator, loc_now.x, loc_now.z)
    return True


def stroll(operator):
    pass


def fleet(operator):
    pass


conscious = \
    {
        "aggressive":
            {
                "Ability": [MobileAbility, BaseCombatAbility],
                "AI": chase_player,
            },
        "calm":
            {
                "Ability": [MobileAbility, BaseCombatAbility],
                "AI": stroll,
            },
    }
