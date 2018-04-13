from panda3d.core import TextNode, TransparencyAttrib


# load a 2d plane model with or without texture
def load_model(tex=None, transparency=True):
    obj = loader.loadModel("models/plane")
    #obj.setBin("unsorted", 0)
    #obj.setDepthTest(False)

    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)

    if tex:
        tex = loader.loadTexture("textures/" + tex)
        obj.setTexture(tex, 1)

    return obj


# recursively read attributes to object
def load_attribute(data_item, attributes):
    # update attributes from the key word (recursively)
    if "key_word" in data_item:
        for keyword in data_item["key_word"]:
            load_attribute(keyword, attributes)

    # update attributes from the database item
    for key in data_item:
        attributes[key] = data_item[key]
