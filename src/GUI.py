from direct.gui.DirectGui import *

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

    # get ready make this object fully ready to work, also been rendered in screen
    def get_ready(self):
        from src.engine import g_engine as engine
        self.hp_bar = DirectWaitBar(barColor=red, value=engine.now_control["hp"],
                                    range=100, pos=hp_bar_pos, frameSize=frameSize, text_scale=text_scale)

    # GUI process the input, eg. when user open the inventory or select the magic
    def handle_key(self, event):
        pass

    # camera focus on the cursor
    def get_focus(self):
        pass

    # camera focus back to player
    def lost_focus(self):
        pass

    # update the GUI values (pre-turn or per-frame)
    def update(self):
        pass
