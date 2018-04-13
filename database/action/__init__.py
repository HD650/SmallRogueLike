# function (callable) instance that can be stored in database objects

# a function wrapper sample for future use
# by binding the parameters, the api in our code can remain unchanged
# eg. "teapot potion":{"onEat": Caller(effect.change_location,random_location_x,random_location_y)}
# reuse the implemented function change_location(re, x, y) and not change its api


class Caller(object):
    def __init__(self, fn, *args, **kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def __call__(self, *uargs, **ukwargs):
        arg = uargs+self._args
        kw = dict(ukwargs.items()+self._kwargs.items())
        self._fn(*arg, **kw)
