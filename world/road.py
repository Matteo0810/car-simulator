from math import *

from helpers.utils import *
from helpers.vector import Vector2


class Road:
    def __init__(self, start: Vector2, end: Vector2, width, start_intersection, end_intersection):
        self._start = start
        self._end = end
        self._width = width
        self._paths = (Path(self, 0), Path(self, 1))
        self._intersections = (start_intersection, end_intersection)
    
    start = property_get("start")
    end = property_get("end")
    width = property_get("width")
    intersections = property_get("intersections")


class Path:
    def __init__(self, road: Road, id_):
        self._id = id_
        self._road = road
    
    @property
    def start(self):
        if self._id:
            return self._road.start + unit_vector(angle_of(self._road.end - self._road.start) - pi) * self._road.width / 4
        else:
            return self._road.end + unit_vector(angle_of(self._road.start - self._road.end) - pi) * self._road.width / 4
    
    @property
    def end(self):
        if not self._id:
            return self._road.start + unit_vector(angle_of(self._road.end - self._road.start) - pi) * self._road.width / 4
        else:
            return self._road.end + unit_vector(angle_of(self._road.start - self._road.end) - pi) * self._road.width / 4
    
    @property
    def intersection(self):
        return self._road.intersections[self._id]
        
