from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *

hb_text_scale = (0.05, 0.05)

hb_frameSize = (-1, 1, -0.03, 0.03)
ms_frameSize = (-0.45, 0.45, -1, 1)
bs_frameSize = (-1, 1, -1, 1)

hb_pos = (0.0, 0.0, 0.90)
ms_pos = (0.25, 0, 0)
bs_pos = (-1, -1, -1)

red = (1.0, 0.0, 0.0, 1.0)
blank = (1.0, 1.0, 1.0, 0.5)
white = (1.0, 1.0, 1.0, 1.0)
black = (0.0, 0.0, 0.0, 1.0)
trans = (1.0, 1.0, 1.0, 0.0)


ms_wordwrap = 20

# handle all GUI staff
class GUI(object):
    def __init__(self):
        self.hp_bar = None
        self.msg_bar = None
        self.base = None
        self.cursor = None

    # get ready make this object fully ready to work, also been rendered in screen
    def get_ready(self):
        from src.engine import g_engine
        #self.base = DirectFrame(frameColor=blank, frameSize=bs_frameSize, pos=bs_pos)
        self.hp_bar = DirectWaitBar(barColor=red, value=100,
                                    range=100, pos=hb_pos, frameSize=hb_frameSize, text_scale=hb_text_scale)
        self.msg_bar = DirectScrolledList(frameColor=blank, pos=ms_pos, numItemsVisible=10)
        self.msg_bar.incButton['frameColor'] = trans
        self.msg_bar.decButton['frameColor'] = trans

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

    # update the GUI values (per-frame)
    def update(self):
        pass

    # update the GUI values (per-turn)
    def turn_update(self):
        from src.engine import g_engine
        self.hp_bar["value"] = g_engine.now_control["Hp"]
