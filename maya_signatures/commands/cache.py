import inspect
import functools


class Memoize(object):
    """cache the return value of a method

    This class is meant to be used as a decorator of methods. The return value
    from a given method invocation will be cached on the instance whose method
    was invoked. All arguments passed to a method decorated with memoize must
    be hashable.

    If a memoized method is invoked directly on its class the result will not
    be cached. Instead the method will be invoked like a static method:
    class Obj(object):
        @memoize
        def add_to(self, arg):
            return self + arg
    Obj.add_to(1) # not enough arguments
    Obj.add_to(1, 2) # returns 3, result is not cached
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return functools.partial(self, obj)

    def __call__(self, *args, **kw):
        obj = args[0]
        try:
            cache = obj.__cache
        except AttributeError:
            cache = obj.__cache = {}
        key = (self.func, args[1:], frozenset(kw.items()))
        try:
            res = cache[key]
        except KeyError:
            res = cache[key] = self.func(*args, **kw)
        return res


class KeyMemoized(object):
    """ Taken from 
        http://stackoverflow.com/questions/10920180/is-there-a-pythonic-way-to-support-keyword-arguments-for-a-memoize-decorator-in
        http://stackoverflow.com/questions/4431703/python-resettable-instance-method-memoization-decorator
        Class is used as a decorator to memoize a given class' method to facilitate caching based on input etc.
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        key = self._key(args, kwargs)

        try:
            return self.cache[key]
        except KeyError:
            print('Could not find key %s in cached values...retrieving...' % key)
            value = self.func(*args)
            self.cache[key] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)

    def _normalize_args(self, args, kwargs):
        spec = inspect.getargs(self.func.__code__).args[1:]
        return dict(kwargs.items() + zip(spec, args))

    @staticmethod
    def _key(args, kwargs):
        # a = self.normalize_args(args, kwargs) # useful for more intense scenarios.
        return ','.join(list(args) + list(kwargs))

    def _reset(self):
        self.cache = {}

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self.func
        return functools.partial(self, obj)
