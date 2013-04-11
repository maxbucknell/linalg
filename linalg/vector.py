from math import sqrt
from numbers import Number
from collections import Iterable

class Vector:
    
    def __init__ (self, *args):
        if len(args) == 1 and isinstance(args[0], Iterable):
            self._v = tuple(args[0])
        else:
            self._v = tuple(args)
    
    @property
    def magnitude (self):
        """The distance between the origin and self."""
        return sqrt(sum( x ** 2 for x in self._v))
    
    @property
    def direction (self):
        """The unit vector in the same direction as self."""
        m = self.magnitude
        return Vector(x / m for x in self._v)
    
    def __getitem__ (self, idx):
        return self._v[idx]
    
    def __iter__ (self):
        return self._v.__iter__()
    
    def __len__ (self):
        return len(self._v)
    
    def __abs__ (self):
        return self.magnitude
    
    def __add__ (self, other):
        return Vector(a + b for a, b in zip(self, other))
    
    def __radd__ (self, other):
        return self + other
    
    def __sub__ (self, other):
        return Vector(a - b for a, b in zip(self, other))
    
    def __rsub__ (self, other):
        return -(self - other)
    
    def __mul__ (self, other):
        if isinstance(other, Number):
            return Vector(other * x for x in self)
        else:
            return NotImplemented
    
    def __rmul__ (self, other):
        return self * other
    
    def __neg__ (self):
        return self * -1
    
    def __str__ (self):
        return ", ".join(str(x) for x in self).join("<>")
    
    def __repr__ (self):
        return "Vector{}".format(repr(self._v))

    def __eq__ (self, other):
        if type(self) == type(other):
            return self._v == other._v
        else:
            return False
    
    def __ne__ (self, other):
        return not self == other

from .matrix import Matrix