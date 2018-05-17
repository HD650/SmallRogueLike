from database.object import material

tiles = \
    {
        "stone_ground":
            {
                "name": "stone ground",
                "key_word": [material.materials["stone"]],
                "texture": "tile/stone_ground.png",
                "canWalk": True,
            },
        "grass_ground":
            {
                "name": "grass ground",
                "key_word": [material.materials["grass"]],
                "texture": "tile/grass_ground.png",
                "canWalk": True
            }
    }