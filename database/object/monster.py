# for test

from database.object.material import materials
from database.object.conscious import conscious

monsters = \
    {
        "stone_dummy":
            {
                "name": "stone dummy",
                "key_word": [materials["stone"], conscious["aggressive"]],
                "texture": "monster.png",
                "transparent": False,
                "collision": True,
            },
    }

