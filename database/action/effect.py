# effects after an action or event occurred


def change_location(re, x, z):
    # import when code excited prevent the cyclic importation
    from engine import g_engine
    loc_now = re.attributes["node"].getPos()
    if re in g_engine.map.map[loc_now.x][loc_now.z]:
        g_engine.map.map[loc_now.x][loc_now.z].remove(re)

    re.attributes["node"].setPos((x, loc_now.y, z))
    g_engine.map.map[x][z].append(re)


def poison(re):
    print(str(re)+" has been poisoned!\n")


def stuck(re):
    print(str(re)+" has been stuck\n")
