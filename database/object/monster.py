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
                "Hp": 1,
                "P_A": 10,
                "P_D": 5,
                "transparent": False,
                "collision": True,
            },
    }

