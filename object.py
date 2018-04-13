from utils import *


class Object:
    def __init__(self, data_item, parent_node):
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
            # if this object has model, render it
            if self.attributes["texture"] is not None:
                self.attributes["node"] = load_model(self.attributes["texture"])
            if self.attributes["node"] is not None:
                self.attributes["node"].reparentTo(parent_node)

