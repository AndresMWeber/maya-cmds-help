import inspect


class KeyMemoized(object):
    """ Taken from 
        http://stackoverflow.com/questions/10920180/is-there-a-pythonic-way-to-support-keyword-arguments-for-a-memoize-decorator-in
        
        Class is used as a decorator to memoize a given class' method to facilitate caching based on input etc.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, object_instance, *args, **kwargs):
        key = self._key(args, kwargs)
        if key not in self.cache:
            print 'Could not find key %s in cached values...retrieving...' % key
            self.cache[key] = self.func(object_instance, *args, **kwargs)
        else:
            print 'Retrieving cached value for input %s' % key
        return self.cache[key]

    def _normalize_args(self, args, kwargs):
        spec = inspect.getargs(self.func.__code__).args[1:]
        return dict(kwargs.items() + zip(spec, args))

    def _key(self, args, kwargs):
        #a = self.normalize_args(args, kwargs) # useful for more intense scenarios.
        return ','.join(list(args)+list(kwargs))