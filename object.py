from utils import *
from panda3d.core import NodePath


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


