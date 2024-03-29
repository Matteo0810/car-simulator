from ctypes import c_float, c_int32, cast, byref, POINTER
from math import pi, copysign
import os


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


def sign(x):
    return 0 if x == 0 else copysign(1, x)


def fast_invsqrt(number):
    x2 = number * 0.5
    y = c_float(number)

    i = cast(byref(y), POINTER(c_int32)).contents.value
    i = c_int32(0x5f3759df - (i >> 1))
    y = cast(byref(i), POINTER(c_float)).contents.value

    y = y * (1.5 - (x2 * y * y))
    return y


def get_path(path):
    path = path.replace('/', '\\')
    return f'{os.path.abspath(".")}\\{path}'


def get_folder_content(path):
    root_dir = get_path(path)
    return [os.path.join(root_dir, file) for file in os.listdir(root_dir)]


def removesuffix(string, suffix):
    if string[len(string)-len(suffix):] == suffix:
        return string[:-len(suffix)]
    return string
