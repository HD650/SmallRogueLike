# test functions to determine whether a action can been preformed


def test_can_move(op, x, y):
    from engine import g_engine
    if x in g_engine.map.map:
        if y in g_engine.map.map[x]:
            return True
    return False


def test_can_eat(op, re):
    if re.attributes["canEat"] is not None:
        return re.attributes["canEat"]
    else:
        return False
