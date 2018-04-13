# actions a player or AI can preform
from database.action.test import *
from database.action.effect import *


def action_move(op, x, y):
    if test_can_move(op, x, y):
        change_location(op, x, y)


def action_eat(op, re):
    if test_can_eat(op, re):
        re.attributes["onEaten"](op)
