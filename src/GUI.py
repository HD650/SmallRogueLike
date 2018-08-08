from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

text_scale = (0.05, 0.05)
frameSize = (-1, 1, -0.03, 0.03)
hp_bar_pos = (0.0, 0.0, 0.95)
red = (1.0, 0.0, 0.0, 1.0)


# helper class for all game message display
class Message(object):
    def __init__(self):
        pass


# handle all GUI staff
class GUI(object):
    def __init__(self):
        self.hp_bar = None
        self.msg_bar = None
        self.cursor = None
        self.animation = None

    # get ready make this object fully ready to work, also been rendered in screen
    def get_ready(self):
        from src.engine import g_engine
        self.animation = Sequence()
        self.hp_bar = DirectWaitBar(barColor=red, value=100,
                                    range=100, pos=hp_bar_pos, frameSize=frameSize, text_scale=text_scale)

    # GUI process the input, eg. when user open the inventory or select the magic
    def handle_menu_key(self, event):
        pass

    # move the cursor and return selected targets
    def handle_aiming_key(self, event, obj, ability):
        from src.engine import g_engine as engine
        pos = engine.camera.getPos()
        if event is "w":
            pos.z += 1
        if event is "s":
            pos.z -= 1
        if event is "a":
            pos.x -= 1
        if event is "d":
            pos.x += 1

        engine.camera.setPos(pos)
        
        if event is "enter":
            player_pos = engine.now_control["node"].getPos()
            player_pos = player_pos + pos
            objects = engine.scene.get_object(player_pos.x, player_pos.z)
            return obj[ability].can_interact_with(objects, player_pos.x, player_pos.z)
            

    # camera focus on the cursor
    def get_focus(self):
        pass

    # camera focus back to player
    def lost_focus(self):
        pass

    # update the GUI values (pre-turn or per-frame)
    def update(self):
        pass
