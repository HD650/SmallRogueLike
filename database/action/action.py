from database.action.test import *
from database.action.effect import *


# TODO this should handle the multi-target selection
# False for action not applied, True for applied
def do_ability(ability, obj, x, y):
    # make sure this object has this ability
    if ability in obj:
        # make sure this object can now apply this ability
        if obj[ability].prerequisites():
            # fetch out all the capable participants of the selected tile
            participants = obj[ability].can_interact_with(None, x, y)
            # if there is no, can't apply the ability
            if participants is None:
                return False
            # if already get enough participants, apply
            elif len(participants) >= obj[ability].participants:
                obj[ability].perform(None)


# Actions or interactions that objects can preform
class InteractionAbility(object):
    def __init__(self, owner_obj):
        super(InteractionAbility, self).__init__()
        self.participants = None
        self.owner = owner_obj
        # is this a positive interaction, if ture, need control to perfrom, and it will comsume one turn
        # eg. talk to other character
        # if false, the interaction will happen automatically when object update
        # eg. fire spread
        self.positive = None

    # determine whether this interaction can happen in this circumstances
    def prerequisites(self):
        raise NotImplementedError

    # test can this interaction perform with the input objects (since the other may not able to do this interaction)
    # TODO arguments should be a dict
    def can_interact_with(self, others, x, y):
        # should return None or at least one object in the others
        raise NotImplementedError

    # do the interaction
    def perform(self, participant):
        raise NotImplementedError

    # do some update every turn
    def update(self):
        # interaction can have no update, which means it will not automatic happen
        pass
    
    # we need use class as the dict key
    def __hash__(self):
        return hash(self.__class__.__name__)

    def __eq__(self, other):
        return issubclass(other, InteractionAbility) and self.__class__.__name__ == other.__class__.__nane__


# ability to able to move on the scene
class MobileAbility(InteractionAbility):
    def __init__(self, owner_obj):
        super(MobileAbility, self).__init__(owner_obj)
        self.positive = True
        self.participants = 0
        # variables this ability need to use should been saved in the owner's attributes
        self.owner["moving_ability"] = True
        self.temp_x = None
        self.temp_y = None

    def prerequisites(self):
        # if the owner can move, then this action can been performed
        return self.owner["moving_ability"]

    def can_interact_with(self, others, x, y):
        if test_can_move(x, y):
            self.temp_x = x
            self.temp_y = y
            return list()
        return None

    def perform(self, participants):
        change_location(self.owner, self.temp_x, self.temp_y)


# ability to able to fight, enable hp, attack, defence, die and many features
# TODO should be divide to more specific abilities like alive ability and combat ability
class BaseCombatAbility(InteractionAbility):
    def __init__(self, owner_obj):
        super(BaseCombatAbility, self).__init__(owner_obj)
        self.positive = True
        self.participants = 1
        # hp
        self.owner["Hp"] = -1
        # physical attack
        self.owner["P_A"] = -1
        # physical defence
        self.owner["P_D"] = 1
        # whether able to combat onw
        self.owner["is_combat"] = True

    def prerequisites(self):
        if self.owner["Hp"] > 0:
            return self.owner["is_combat"]
        else:
            return False

    def can_interact_with(self, others, x, y):
        cur_pos = self.owner["node"].getPos()
        cur_pos.x -= x
        cur_pos.z -= y
        if abs(cur_pos.x) > 1 or abs(cur_pos.z) > 1:
            print("You can attack objects two blocks away from you.")
            return None
        result = list()
        for one in others:
            if "Ability" in one:
                if BaseCombatAbility in one["Ability"]:
                    result.append(one)
        if len(result) is 0:
            print("There is no objects to attack!")
        return result

    def perform(self, participants):
        defence =participants[0][BaseCombatAbility].get_physical_defence()
        attack = self.get_physical_attack()
        damage = max(attack - defence, 0)
        print("%s attacks %s with damage %d" % (self.owner, participants[0], damage))

    def update(self):
        if self.owner["Hp"] <= 0:
            self.owner["is_combat"] = False
            # do death logic, spawn died body etc
            pass

    def get_physical_attack(self):
        return self.owner["P_A"]

    def get_physical_defence(self):
        return self.owner["P_D"]
