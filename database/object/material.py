import database.action.effect as effect

materials = \
    {
        "stone":
            {
                "canOnFire": False,
                "canEat": True,
                "onEaten": effect.stuck,
            },
        "grass":
            {
                "canOnFire": True,
                "canEat": True,
                "onEaten": effect.poison,
            }
    }