# actions a player or an object can preform
from database.action.test import *
from database.action.effect import *


def action_move(operator, x, y):
    if test_can_move(operator, x, y):
        change_location(operator, x, y)


def action_eat(operator, receiver):
    if test_can_eat(operator, receiver):
        receiver["onEaten"](operator)
