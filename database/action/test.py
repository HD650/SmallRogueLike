# test functions to determine whether a action can been preformed


def test_tile_opaque(x, y):
    from src.engine import g_engine
    if g_engine.scene.tran_bitmap[x][y]:
        return False
    else:
        return True


def test_can_move(x, y):
    from src.engine import g_engine
    if x in g_engine.scene.map:
        if y in g_engine.scene.map[x]:
            if not g_engine.scene.coll_bitmap[x][y]:
                return True
    return False


def test_can_eat(operator, receiver):
    if receiver.attributes["canEat"] is not None:
        return receiver.attributes["canEat"]
    else:
        return False
