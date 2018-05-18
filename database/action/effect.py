# effects after an action or event occurred


def change_location(receiver, x, z):
    # import when code excited prevent the cyclic importation
    from engine import g_engine
    loc_now = receiver.attributes["node"].getPos()
    if receiver in g_engine.map.map[loc_now.x][loc_now.z]:
        g_engine.map.map[loc_now.x][loc_now.z].remove(receiver)

    receiver.attributes["node"].setPos((x, loc_now.y, z))
    g_engine.map.map[x][z].append(receiver)


def poison(receiver):
    print(str(receiver) + " has been poisoned!\n")


def stuck(receiver):
    print(str(receiver) + " has been stuck\n")
