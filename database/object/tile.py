# tiles are objects that form the scene

from database.object.material import materials

tiles = \
    {
        "stone_wall":
            {
                "name": "stone wall",
                "key_word": [materials["stone"]],
                "texture": "tile/stone_wall.png",
                "collision": True,
                "transparent": False,
            },
        "grass_ground":
            {
                "name": "grass ground",
                "key_word": [materials["grass"]],
                "texture": "tile/grass_ground.png",
                "collision": False,
                "transparent": True,
            },
        "fog_of_war":
            {
                "name": "fog of war",
                "texture": None,
                'visited': False,
            }
    }