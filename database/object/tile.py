from database.object import material

tiles = \
    {
        "stone_ground":
            {
                "key_word": [material.materials["stone"]],
                "texture": "tile/stone_ground.png",
                "canWalk": True,
            },
        "grass_ground":
            {
                "key_word": [material.materials["grass"]],
                "texture": "tile/grass_ground.png",
                "canWalk": True
            }
    }