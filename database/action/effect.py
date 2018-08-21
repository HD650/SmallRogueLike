# effects after an action or event occurred
from direct.interval.IntervalGlobal import *
from src.utils import *


def change_location(receiver, x, z):
    # import when code excited prevent the cyclic importation
    from src.engine import g_engine
    loc_now = receiver["node"].getPos()
    g_engine.scene.move_object(receiver, loc_now.x, loc_now.z, x, z)
    loc_now.x = x
    loc_now.z = z

    animation = LerpPosInterval(receiver["node"], 0.1, loc_now, blendType='noBlend')
    g_engine.animation.append(animation)

def close_combat_damage(attacker, receiver, damage):
    receiver["Hp"] -= damage
    from src.engine import g_engine
    attacker_pos = attacker["node"].getPos() 
    defencer_pos = receiver["node"].getPos()
    animation = Sequence()
    animation.append(LerpPosInterval(attacker["node"], 0.05, defencer_pos, blendType='noBlend'))
    animation.append(LerpPosInterval(attacker["node"], 0.05, attacker_pos, blendType='noBlend'))
    g_engine.animation.append(animation)
    add_message("%s attacks %s with damage %d" % (attacker, receiver, damage))


def poison(receiver):
    add_message(str(receiver) + " has been poisoned!\n")


def stuck(receiver):
    add_message(str(receiver) + " has been stuck\n")
