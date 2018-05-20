# test functions to determine whether a action can been preformed


def test_tile_opaque(x, y):
    from engine import g_engine
    if g_engine.map.map[x][y][0].attributes["transparent"]:
        return False
    else:
        return True


def test_can_move(operator, x, y):
    from engine import g_engine
    if x in g_engine.map.map:
        if y in g_engine.map.map[x]:
            return True
    return False


def test_can_eat(operator, receiver):
    if receiver.attributes["canEat"] is not None:
        return receiver.attributes["canEat"]
    else:
        return False
