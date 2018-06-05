# utilize function wrapper can achieve the perk system very easily
# first, we can do almost anything in the wrapper function code, so the perks can have powerful functionality
# second, we can wrapper any function or method in the code, so perks can change the game logic everywhere
# third, the wrapper won't destroy the previous wrapper, so we can have many perks combined together

import types


# perk use function wrapper to decorate the original method so the method has new behaviour
class DoubleDamagePerk:
    # when player get a perk, the perk replace the player's original deal_damage method with a new one,
    # the new one will double the player's attack and then deal the damage
    def __call__(self, *args, **kwargs):
        # a decorator function
        def double_dam_decorator(func):
            # this new_func will replace the original deal_damage method in player
            # attention, new_func should have same argument list with the original one
            def new_func(player, enemy):
                # do some thing special, double attack, cast an explosion, heath stealing, spawn a summon etc.
                player.attack *= 2
                # call original method, our perk just add some new feature but not implement the original feature
                # attention, since the func here is already a bond function, we don't need to pass the self to it
                # func(enemy) is actually player.deal_damage(self, enemy)
                func(enemy)
                player.attack /= 2
            # return the new deal_function instance
            return new_func
        # decorate the old method
        new_function = double_dam_decorator(args[0].deal_damage)
        # replace the original player method
        # attention, use types here to bind the player instance to the first argument "self" to new_function,
        # so the normal static function become a method of player
        args[0].deal_damage = types.MethodType(new_function, args[0])


class Player:
    def __init__(self):
        self.attack = 10
        self.defence = 10
        self.hp = 100

    # a function do the original game logic
    def deal_damage(self, enemy):
        dam = self.attack - enemy.defence
        enemy.hp -= dam
        print("deal {0} damage to enemy".format(dam))

    # player get a perk and the perk give player some powerful change
    def get_perk(self, perk):
        perk(self)
        print("get double damage perk")


class Enemy:
    def __init__(self):
        self.attack = 5
        self.defence = 5
        self.hp = 100

if __name__ == '__main__':
    me = Player()
    it = Enemy()
    # original game logic will cause 5 damage to enemy
    me.deal_damage(it)
    print("enemy remain hp of it {0}".format(it.hp))

    # the perk add a function wrapper to the player deal_damage method, and now deal_damage method deal double damage
    me.get_perk(DoubleDamagePerk())
    me.deal_damage(it)
    print("enemy remain hp of it {0}".format(it.hp))