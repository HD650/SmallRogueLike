from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import Sequence, Func

from src.scene import Scene
from src.GUI import GUI


class ControlState(FSM):
    def __init__(self):
        FSM.__init__(self, 'ControlState')
        self.GUI = GUI()
        self.action_stack = []
        self.participants = []

    # player can move and fight
    def enterMove(self):
        pass

    # player open the menu
    def enterMenu(self):
        pass

    # begin to select targets
    def start_aiming(self, obj, ability):
        # add the waiting action to stack
        self.action_stack.append((obj, ability))
        self.participants = []
        self.request('Aiming')

    # player has finished selecting targets, apply the action
    def finish_aiming(self):
       obj, ability = self.action_stack[-1]
       # perform the action
       obj[ability].perform(self.participants)
       self.action_stack = []
       self.participants = []
       self.request('Move')

    # player do aiming
    def enterAiming(self):
        # spawn a cursor at the center
        pass

    def exitAiming(self):
        # set back camera position
        from src.engine import g_engine
        pos = g_engine.camera.GetPos()
        pos.x = 0
        pos.z = 0
        g_engine.camera.SetPos(pos)

    # update the ui every frame
    def update(self, task):
        self.GUI.update()

    # handle the input key
    def handle_key(self, event):
        from src.engine import g_engine as engine
        if self.state == 'Move':
            engine.now_control.handle_key(event)
            # true for next turn
            return True
        elif self.state == 'Aiming':
            # return the selected target
            # TODO make sure handle will only return one target
            obj, ability = self.action_stack[-1]
            result = self.GUI.handle_aiming_key(event, obj, ability)
            # if we found targets, add them to participants
            if result is not None and len(result) > 0:
                self.participants.extend(result)
            if len(self.participants) >= ability.participants:
                self.finish_aiming()
                # true for next turn
                return True
            return False
        elif self.state == 'Menu':
            return self.GUI.handle_menu_key(event)


class SceneState(FSM):
    def __init__(self):
        FSM.__init__(self, 'SceneState')
        self.control_state = ControlState()
        self.defaultTransitions = {
            'Player': ['AI'],
            'AI': ['Player'],
        }
        self.ai_move = None
        self.player_move = None

    # player turn
    def enterPlayer(self):
        print("Player turn start\n")
        from src.engine import g_engine
        g_engine.scene.turn_update()
        self.player_move = False
        self.control_state.request("Move")

    def exitPlayer(self):
        print("Player turn end\n")
        # do turn clearing here
        from src.engine import g_engine
        g_engine.scene.update_mask()

    # AI turn
    def enterAI(self):
        print("AI turn start\n")
        from src.engine import g_engine
        g_engine.scene.turn_update()
        self.ai_move = False

    def exitAI(self):
        print("AI turn end\n")
        # do turn clearing here
        from src.engine import g_engine
        g_engine.scene.update_mask()

    def update(self, task):
        if self.state == "Player":
            # player move
            self.control_state.update(task)
        elif self.state == "AI":
            # ai will move only once pre turn, so if the ai has moved and currently in an animation(still in AI state),
            # we do not move it again but wait until the animation end and the state transferred
            if not self.ai_move:
                # do the AI staff
                from src.engine import g_engine as engine
                for ai in engine.scene.conscious_objects:
                    ai["AI"](ai)
                self.transfer_player()

    def handle_key(self, event):
        # if this is AI turn, ignore the key
        if self.state == "AI":
            return
        elif self.state == "Player":
            # player will move only once pre turn
            if not self.player_move:
                next_turn = self.control_state.handle_key(event)
                # if player input a key that will end this turn, switch to AI turn
                if next_turn:
                    self.transfer_ai()

    def transfer_ai(self):
        # transfer state from player to ai
        from src.engine import g_engine
        temp = g_engine.animation
        g_engine.animation = Sequence()
        # do all the object animations and then transfer the state
        g_engine.animation.append(temp)
        g_engine.animation.append(Func(self.request, "AI"))
        g_engine.animation.start()
        # refresh the animation buffer
        g_engine.animation = type(temp)()
        self.player_move = True

    def transfer_player(self):
        # transfer state from ai to player
        from src.engine import g_engine
        temp = g_engine.animation
        g_engine.animation = Sequence()
        # do all the object animations and then transfer the state
        g_engine.animation.append(temp)
        g_engine.animation.append(Func(self.request, "Player"))
        g_engine.animation.start()
        # refresh the animation buffer
        g_engine.animation = type(temp)()
        self.ai_move = True


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
        from src.engine import g_engine as engine
        engine.scene = Scene()
        engine.scene.get_ready()
        engine.scene.add_player(engine.now_control, 0, 0)
        # player turn
        self.scene_state.request("Player")
        pass

    def exitScene(self):
        print("Exit scene map\n")
        from src.engine import g_engine as engine
        # TODO here we should change the map to global map
        engine.scene = None
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
