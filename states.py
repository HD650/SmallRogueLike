from direct.fsm.FSM import FSM
from scene import Scene


class ControlState(FSM):
    def __init__(self):
        FSM.__init__(self, 'ControlState')

    # player can move and fight
    def enterMove(self):
        pass

    # player open the menu
    def enterMenu(self):
        pass

    # player do amming
    def enterAimming(self):
        pass

    # handle the input key
    def handle_key(self, event):
        from engine import g_engine as engine
        engine.player.handle_key(event)
        return False


class SceneState(FSM):
    def __init__(self):
        FSM.__init__(self, 'SceneState')
        self.control_state = ControlState()

    # player turn
    def enterPlayer(self):
        print("Player turn start\n")
        pass

    # player turn end
    def exitPlayer(self):
        print("Player turn end\n")
        pass

    # AI turn
    def enterAI(self):
        print("AI turn start\n")
        pass

    # AI turn end
    def exitAI(self):
        print("AI turn end\n")
        pass

    def update(self, task):
        if self.state == "Player":
            # player move
            pass
        else:
            # do the AI staff
            pass

    def handle_key(self, event):
        # if this is AI turn, ignore the key
        if self.state == "AI":
            return
        elif self.state == "Player":
            next_turn = self.control_state.handle_key(event)
            # if player input a key that will end this turn, switch to AI turn
            if next_turn:
                self.request("AI")


class GameState(FSM):
    def __init__(self):
        FSM.__init__(self, 'GameState')
        self.scene_state = SceneState()

    def enterGlobal(self):
        print("Enter global map\n")
        pass

    def exitGlobal(self):
        print("Exit global map\n")
        pass

    def enterScene(self):
        print("Enter scene map\n")
        # init the scene, spawn player in the scene
        from engine import g_engine as engine
        engine.map = Scene()
        engine.map.get_ready()
        engine.map.add_player(engine.player, 0, 0)
        # player turn
        self.scene_state.request("Player")
        pass

    def exitScene(self):
        print("Exit scene map\n")
        from engine import g_engine as engine
        # TODO here we should change the map to global map
        engine.map = None
        # clean up the scene state to off
        self.scene_state.cleanup()
        pass

    def update(self, task):
        if self.state == "Scene":
            self.scene_state.update(task)
        else:
            pass

    def handle_key(self, event):
        if self.state == "Scene":
            self.scene_state.handle_key(event)
