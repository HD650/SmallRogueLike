# effects after an action or event occurred
from direct.interval.IntervalGlobal import *


def change_location(receiver, x, z):
    # import when code excited prevent the cyclic importation
    from src.engine import g_engine
    loc_now = receiver["node"].getPos()
    g_engine.scene.move_object(receiver, loc_now.x, loc_now.z, x, z)
    loc_now.x = x
    loc_now.z = z

    animation = LerpPosInterval(receiver["node"], 0.1, loc_now, blendType='noBlend')
    g_engine.animation.append(animation)


def poison(receiver):
    print(str(receiver) + " has been poisoned!\n")


def stuck(receiver):
    print(str(receiver) + " has been stuck\n")
