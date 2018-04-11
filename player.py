from object import Object
from utils import *


class Player(Object):
    def __init__(self):
        self.hp = 100
        self.mp = 100
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = 5
        self.node = loadObject("ship.png")

    def key(self, event):
        pos = self.node.getPos()
        if event is "w":
            pos.z += 1
        if event is "s":
            pos.z -= 1
        if event is "a":
            pos.x -= 1
        if event is "d":
            pos.x += 1
        self.node.setPos(pos)

    def update(self, task):
        pass
