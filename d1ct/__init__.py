__description__ = "dict implementation supporting attribute access, recursion, json, hashable, subclass, metaclass"
__version__ = "1.0.4"
__long_description__ = """

▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██████╗▒▒██╗▒██████╗████████╗▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██╔══██╗███║██╔════╝╚══██╔══╝▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██║▒▒██║╚██║██║▒▒▒▒▒▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██║▒▒██║▒██║██║▒▒▒▒▒▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒██████╔╝▒██║╚██████╗▒▒▒██║▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒╚═════╝▒▒╚═╝▒╚═════╝▒▒▒╚═╝▒▒▒▒▒▒▒▒▒
 ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒▓▒

d1ct is a hybrid object/mapping.

 - directly inherited from dict
 - accessible by attribute.   o.x == o['x'] 
 - This works also for all corner cases.
 - json.dumps json.loads
 - vars() works on it!
 - hashable! (should not yet trust on it, though)
 - autocomplete works even if the objects comes from a list
 - best of all, it works recursively. So all inner dicts will become d1cts too.
"""


from collections.abc import Mapping as _Mapping, Sequence as _Sequence

_DEBUGMODE = False

__all__ = ["d1ct"]


class d1ct(dict):
    """
    """

    __module__ = None

    def __init__(self, *args, **kwargs):
        """
        d1ct() -> new empty d1ct
        d1ct(mapping) -> new d1ct initialized from a mapping object's
            (key, value) pairs
        d1ct(iterable) -> new d1ct initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        d1ct(**kwargs) -> new d1ct initialized with the name=value pairs
            in the keyword argument list.  For example:  d1ct(one=1, two=2)
        """
        if _DEBUGMODE:
            _dbgprint(self, *args, **kwargs)
        super().__init__()
        _ = dict({
            k: v for k, v in self.__class__.__dict__.items()
            if (type(k) is str and not k.startswith('_')) and not callable(v)
        })
        _.update(*args, **kwargs)
        for k, v in _.items():
            super().__setitem__(k, _wrap(v))
        super().__setattr__("__dict__", self)
        
    def __setitem__(self, key, value):
        if _DEBUGMODE:
            _dbgprint(self, key, value)
        super().__setitem__(key, _wrap(value))

    def __setattr__(self, key, value):
        if _DEBUGMODE:
            _dbgprint(self, key, value)
        super().__setitem__(key, _wrap(value))

    def __missing__(self, key):
        if _DEBUGMODE:
            _dbgprint(self, key)
        raise AttributeError(f"{self.__class__} has no attribute '{key}'")

    def __getattribute__(self, item):
        if _DEBUGMODE:
            print("__getattribute__", item)
        return super().__getattribute__(item)

    def __call__(self, *args, **kwargs):
        if _DEBUGMODE:
            _dbgprint(self, *args, **kwargs)
        return self.__class__(*args, **kwargs)

    def update(self, *a, **kw):
        """
        small change compared to dicts .update method
        """
        if _DEBUGMODE:
            _dbgprint(self, *a, **kw)
        d = {}
        if len(a) > 0:
            a = a[0]
            d.update(a)
            if isinstance(a, (str, bytes)):
                pass
        if kw:
            d.update(kw)
        for k, v in d.items():
            if isinstance(v, dict):
                d[k] = d1ct(v)
            elif isinstance(v, (list, set, tuple, frozenset)):
                d[k] = [d1ct(i) for i in v]
        super(d1ct, self).update(d)

    def __hash__(self, opt=None):
        if _DEBUGMODE:
            _dbgprint(self, opt=opt)
        tohash = set()
        for i, k in enumerate(self):
            v = self[k]
            if not isinstance(v, (list, set)):
                tohash.add(v)
            else:
                [tohash.add(iv) for iv in v]
        return hash(frozenset(tohash))

    def __dir__(self):
        if _DEBUGMODE:
            _dbgprint(self)
        return list(map(str, super(d1ct, self).__dir__()))


def _wrap(v):
    if isinstance(v, _Mapping):
        v = d1ct(v)
    elif isinstance(v, _Sequence) and not isinstance(
        v, (str, bytes, bytearray, set, tuple)
    ):
        v = list([_wrap(x) for x in v])
    return v


def _dbgprint(obj, *a, **kw):
    """
    dumb debug printer

    :param obj: instance when called from a method ( like _dbgprint(self, *args, **kwargs) )
    :param *a: args
    :param **kw: kwargs
    :return: None
    """

    import inspect

    caller = inspect.stack()[1].function
    callercls = obj.__class__.__name__
    astr, kwstr, cstr = "", "", ""
    if len(a) > 0:
        astr = str(a)[1:-1]
    if len(a) <= 1:
        astr = astr.replace(",", "")
    if len(kw) > 0:
        for k, v in kw.items():
            kwstr += k.replace("'", "")
            kwstr += "="
            kwstr += str(v)
    if astr and kwstr:
        cstr = ", "
    print(f"called  {callercls}.{caller}({astr}{cstr}{kwstr})")



import sys
sys.modules[__name__] = d1ct
