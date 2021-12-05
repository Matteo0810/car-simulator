from pygame import Vector2
from math import cos, sin, atan2, pi


def unit_vector(angle: float, length: float = 1):
    return Vector2(cos(angle), sin(angle)) * length


def angle_of(vector: Vector2):
    return atan2(vector.y, vector.x)


def nice_angle(rad):
    return (rad + pi) % (2 * pi) - pi


def lerp(a, b, m):
    return a * m + b * (1 - m)


def getter(name):
    return lambda obj: obj.__dict__[name]


def _set(obj, name, value):
    obj.__dict__[name] = value


def setter(name):
    return lambda obj, value: _set(obj, name, value)


def property_get(name):
    return property(getter("_" + name))


def property_getset(name):
    return property(getter("_" + name), setter("_" + name))
