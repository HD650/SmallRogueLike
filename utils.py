from panda3d.core import TextNode, TransparencyAttrib

global_models = dict()


# load a 2d plane model with or without texture
def load_model(texture=None, transparency=True):
    if texture is None:
        texture = 'None'
    # if we already have the required model, do not load again
    if texture in global_models:
        return global_models[texture]
    # else load the model and save in a global dict for the all future use
    else:
        obj = loader.loadModel("models/plane")
        #obj.setBin("unsorted", 0)
        #obj.setDepthTest(False)

        if transparency:
            obj.setTransparency(TransparencyAttrib.MAlpha)

        if texture == 'None':
            pass
        else:
            tex = loader.loadTexture("textures/" + texture)
            obj.setTexture(tex, 1)

        global_models[texture] = obj
        return global_models[texture]


# recursively read attributes to object
def load_attribute(data_item, attributes):
    # update attributes from the key word (recursively)
    if "key_word" in data_item:
        for keyword in data_item["key_word"]:
            load_attribute(keyword, attributes)

    # update attributes from the database item
    for key in data_item:
        attributes[key] = data_item[key]
