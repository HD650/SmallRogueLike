from panda3d.core import NodePath

from src.utils import *


class Object(dict):
    def __init__(self, data_item, parent_node, x=0, y=0):
        super(Object, self).__init__(self)

        if data_item is not None:
            # load attributes from database
            load_attribute(data_item, self)

        # load the model and instance it in the scene
        model = load_model(self["texture"])
        self["model"] = model
        if parent_node is not None:
            # use placeholder and instance api to reuse model
            self["node"] = parent_node.attachNewNode(str(self))
        else:
            self["node"] = NodePath(str(self))
        self["node"].setPos(x, 0, y)
        # objects with same model shared the model data
        model.instanceTo(self["node"])

        # set datastructure for all candidate interactions for this object
        # used for optimize off a lot invalid interactions this turn
        if "Ability" in self:
            self["PositiveInteractSet"] = set()
            self["PassiveInteractSet"] = set()

    def turn_update(self):
        # make sure this object has some abilities
        if "Ability" in self:
            for ab in self["Ability"]:
                # update candidate interact set
                if self[ab].prerequisites():
                    if self[ab].positive:
                        self["PositiveInteractSet"].add(ab)
                    else:
                        self["PassiveInteractSet"].add(ab)
                else:
                    if self[ab].positive:
                        self["PositiveInteractSet"].discard(ab)
                    else:
                        self["PassiveInteractSet"].discard(ab)
        # TODO buffer staff
        pass

    def __str__(self):
        return self["name"]
