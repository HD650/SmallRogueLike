# tiles are objects that form the scene

from database.object.material import materials

tiles = \
    {
        "stone_ground":
            {
                "name": "stone ground",
                "key_word": [materials["stone"]],
                "texture": "tile/stone_ground.png",
                "canWalk": True,
                "transparent": True,
            },
        "grass_ground":
            {
                "name": "grass ground",
                "key_word": [materials["grass"]],
                "texture": "tile/grass_ground.png",
                "canWalk": True,
                "transparent": True,
            },
        "fog_of_war":
            {
                "name": "name of fog",
                "texture": None,
            }
    }