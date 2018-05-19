# effects after an action or event occurred
from direct.interval.IntervalGlobal import *


def change_location(receiver, x, z):
    # import when code excited prevent the cyclic importation
    from engine import g_engine
    loc_now = receiver.attributes["node"].getPos()
    if receiver in g_engine.map.map[loc_now.x][loc_now.z]:
        g_engine.map.map[loc_now.x][loc_now.z].remove(receiver)

    loc_now.x = x
    loc_now.z = z
    # receiver.attributes["node"].setPos(loc_now)
    g_engine.map.map[x][z].append(receiver)

    animation = LerpPosInterval(receiver.attributes["node"], 0.2, loc_now, blendType='noBlend')
    g_engine.animation.append(animation)


def poison(receiver):
    print(str(receiver) + " has been poisoned!\n")


def stuck(receiver):
    print(str(receiver) + " has been stuck\n")
