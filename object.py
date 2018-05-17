from utils import *


class Object:
    def __init__(self, data_item, parent_node, x=0, y=0):
        # basic attributes
        self.attributes = dict()
        self.attributes["height"] = 1
        self.attributes["volume"] = 1
        self.attributes["value"] = 0
        self.attributes["texture"] = "default.png"
        self.attributes["node"] = None
        self.attributes["update"] = []

        if data_item is not None:
            # load attributes from database
            load_attribute(data_item, self.attributes)
            # if this object has model and , instance it in the scene
            if self.attributes["texture"] is not None:
                # use placeholder and instance api to reuse model
                self.attributes["node"] = parent_node.attachNewNode(str(self))
                self.attributes["node"].setPos(x, 0, y)
                model = load_model(self.attributes["texture"])
                # objects with same model shared the model data
                model.instanceTo(self.attributes["node"])

