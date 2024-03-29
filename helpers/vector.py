import math
import struct

from helpers.utils import fast_invsqrt


def bits(f: float):
    s = struct.pack('>f', f)
    return struct.unpack('>l', s)[0]


class Vector2:
    def __init__(self, x, y):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return 0

    def length_squared(self):
        return self.x ** 2 + self.y ** 2

    def length(self):
        return math.sqrt(self.length_squared())

    def distance_squared(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2

    def distance(self, other):
        if type(other) is Vector3:
            return other.distance(self)
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def normalize(self):
        return self / self.length() if self != Vector2(0, 0) else Vector2(0, 0)

    def fast_normalize(self):
        return self * fast_invsqrt(self.length_squared())

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def angle(self, other=None):
        if other:
            return (self.angle() - other.angle()) % (2 * math.pi) - math.pi
        else:
            return math.atan2(self._y, self._x)

    @staticmethod
    def of_angle(angle, length=1):
        return Vector2(math.cos(angle), math.sin(angle)) * length

    def __iter__(self):
        return [self.x, self.y].__iter__()

    def __repr__(self):
        return f"Vector2(*{(self.x, self.y)})"

    def __add__(self, other):
        if other == 0 or other is None:
            return self
        if not isinstance(other, Vector2):
            raise TypeError()
        return self.__class__(self.x + other.x, self.y + other.y)

    __radd__ = __add__

    def __sub__(self, other):
        if other == 0 or other is None:
            return self
        if not isinstance(other, Vector2):
            raise TypeError()
        return self.__class__(self.x - other.x, self.y - other.y)

    __rsub__ = __sub__

    def __mul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise TypeError()
        return self.__class__(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise TypeError()
        return self.__class__(self.x / other, self.y / other)

    __rtruediv__ = __truediv__

    def __eq__(self, other):
        if not isinstance(other, Vector2):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Vector2(x={self.x}, y={self.y})'

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __hash__(self):
        return ((bits(self.x) * 73856093) ^ (bits(self.y) * 19349663)) % 0x80000000


class Vector3:
    def __init__(self, x, y, z):
        self._x = float(x)
        self._y = float(y)
        self._z = float(z)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def xy(self):
        return Vector2(self.x, self.y)

    def length_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def length(self):
        return math.sqrt(self.length_squared())

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)

    def normalized(self):
        return self / self.length() if self != Vector3(0, 0, 0) else Vector3(0, 0, 0)

    def fast_normalized(self):
        return self * fast_invsqrt(self.length_squared())

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def __repr__(self):
        return f"Vector3(*{(self.x, self.y, self.z)})"

    def __iter__(self):
        return [self.x, self.y, self.z].__iter__()

    def __add__(self, other):
        if other == 0 or other is None:
            return self
        if not isinstance(other, Vector3):
            raise TypeError()
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, Vector3):
            raise TypeError()
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    __rsub__ = __sub__

    def __mul__(self, other):
        if type(other) is not int and type(other) is not float:
            raise TypeError()
        return self.__class__(self.x * other, self.y * other, self.z * other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if type(other) is not int and type(other) is not float:
            raise TypeError()
        return self.__class__(self.x / other, self.y / other, self.z / other)

    __rtruediv__ = __truediv__

    def __eq__(self, other):
        if not isinstance(other, Vector3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return f'Vector3(x={self.x}, y={self.y}, z={self.z})'

    def __neg__(self):
        return self.__class__(-self.x, -self.y, -self.z)

    def __hash__(self):
        return ((bits(self.x) * 73856093) ^ (bits(self.y) * 19349663) ^ (bits(self.z) * 83492791)) % 0x80000000

    @staticmethod
    def from_vector2(vector2: Vector2, z=0):
        x, y = vector2
        return Vector3(x, y, z)
