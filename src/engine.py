from direct.interval.IntervalGlobal import Parallel
from direct.showbase.ShowBase import ShowBase
from src.GUI import GUI
from panda3d.core import OrthographicLens

from src.player import Player
from src.states import GameState

window_ratio = 4/3
window_height = 30
window_width = window_height*window_ratio

player_z = -2
object_z = -1
tiles_z = 0
mask_z = -3
camera_z = -64


# TODO decouple with the ShowBase, to be engine unrelated
class Engine(ShowBase):
    def __init__(self):
        # open a window
        ShowBase.__init__(self)
        # important object maintained by engine
        self.scene = None
        self.player = None
        self.now_control = None
        self.game_state = None
        self.GUI = None
        self.animation = None

        # disable the panda3d default mouse rotation
        self.disableMouse()
        # camera debug
        # self.oobe()
        lens = OrthographicLens()
        lens.setFilmSize(window_width, window_height)  # Or whatever is appropriate for your scene
        self.cam.node().setLens(lens)
        self.camera.setPos(0, camera_z, 0)

        # ready the keyboard event
        self.accept("arrow_left", self.handle_key, ["a"])
        self.accept("arrow_right", self.handle_key, ["d"])
        self.accept("arrow_up", self.handle_key, ["w"])
        self.accept("arrow_down", self.handle_key, ["s"])
        self.accept("space", self.handle_key, ["space"])
        self.accept("enter", self.handle_key, ["enter"])
        self.accept("escape", self.handle_key, ["escape"])

    # TODO the engine get ready do not need to init the scene, this should be done in the state machine
    def get_ready(self):
        # let gui get ready first, since state machine need a reference of it
        self.GUI = GUI()
        self.GUI.get_ready()
        # load a scene and add player to it
        self.game_state = GameState()
        self.player = Player()
        # the object we control may not be player, so we need another variable
        self.now_control = self.player
        # animation will be play parallel
        self.animation = Parallel()
        # enable pre-frame update function
        self.task_mgr.add(self.update, "game_update")
        # enter first state of the game
        self.game_state.request("Scene")

    def handle_key(self, event):
        self.game_state.handle_key(event)
        pass

    def update(self, task):
        # update all the game
        self.game_state.update(task)
        return task.cont

# the engine singleton
g_engine = Engine()

