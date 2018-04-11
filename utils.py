from panda3d.core import TextNode, TransparencyAttrib
from panda3d.core import NodePath


def loadObject(tex=None, transparency=True):
    obj = loader.loadModel("models/plane")
    obj.setBin("unsorted", 0)
    obj.setDepthTest(False)

    if transparency:
        obj.setTransparency(TransparencyAttrib.MAlpha)

    if tex:
        tex = loader.loadTexture("textures/" + tex)
        obj.setTexture(tex, 1)

    return obj
