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
        # is this a action(positive) or passive interaction
        self.positive = None
        self.participants = None
        self.owner = owner_obj

    # determine whether this interaction can happen in this circumstances
    def prerequisites(self):
        raise NotImplementedError

    # test can this interaction perform with the input objects (since the other may not able to do this interaction)
    def can_interact_with(self, others, x, y):
        # should return None or at least one object in the others
        raise NotImplementedError

    # do the interaction
    def perform(self, participant):
        raise NotImplementedError

    # we need use class as the dict key
    def __hash__(self):
        return hash(self.__class__.__name__)

    def __eq__(self, other):
        return issubclass(other, InteractionAbility) and self.__class__.__name__ == other.__class__.__nane__


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
