from panda3d.core import TextNode, TransparencyAttrib
from direct.gui.DirectGui import *
from src.GUI import *

global_models = dict()

# add a message on the screen
def add_message(string):
    from src.engine import g_engine
    item = DirectLabel(text = str(string), text_scale=hb_text_scale, frameColor=trans, text_fg=white, text_wordwrap=ms_wordwrap, text_align=TextNode.ALeft, text_shadow=black)
    key = g_engine.GUI.msg_bar.addItem(item, 1)
    g_engine.GUI.msg_bar.scrollToItemID(key, True)

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
def load_attribute(data_item, obj):
    # update attributes from the key word (recursively)
    if "key_word" in data_item:
        for keyword in data_item["key_word"]:
            load_attribute(keyword, obj)

    # load the abilities to this object
    if "Ability" in data_item:
        for ability in data_item["Ability"]:
            temp = ability(obj)
            obj[ability] = temp

    # update attributes from the database item
    for key in data_item:
        obj[key] = data_item[key]
