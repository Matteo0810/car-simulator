from engine.scene.models import Models
from helpers.utils import *
from helpers.vector import Vector2
from helpers.dotenv import get_env


def _dist(x1, y1, x2, y2, x3, y3):  # x3,y3 is the point
    """
        retourne la distance entre le point (x3, y3) et le plus proche point du segment [(x1, y1), (x2, y2)]
    """
    px = x2-x1
    py = y2-y1

    norm = px*px + py*py

    u = ((x3 - x1) * px + (y3 - y1) * py) / float(norm)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    dist_squared = (dx*dx + dy*dy)

    return dist_squared ** 0.5


class Road:
    def __init__(self, start: Vector2, end: Vector2, speed_limit, start_intersection, end_intersection):
        self._start = start
        self._end = end
        self._speed_limit = speed_limit
        self._paths = (Path(self, 0), Path(self, 1))
        self._intersections = (start_intersection, end_intersection)

    start = property_get("start")
    end = property_get("end")
    speed_limit = property_get("speed_limit")
    intersections = property_get("intersections")
    paths = property_get("paths")
    
    def contains(self, position):
        return self._paths[0].contains(position) or self._paths[1].contains(position)


class Path:
    def __init__(self, road: Road, id_):
        self._id = id_
        self._road = road

    @property
    def start(self):
        if self._id:
            return self._road.start + Vector2.of_angle((self._road.end - self._road.start).angle() - pi) * get_env(
                "ROAD_WIDTH") / 4
        else:
            return self._road.end + Vector2.of_angle((self._road.start - self._road.end).angle() - pi) * get_env(
                "ROAD_WIDTH") / 4

    @property
    def end(self):
        if not self._id:
            return self._road.start + Vector2.of_angle((self._road.end - self._road.start).angle() - pi) * get_env(
                "ROAD_WIDTH") / 4
        else:
            return self._road.end + Vector2.of_angle((self._road.start - self._road.end).angle() - pi) * get_env(
                "ROAD_WIDTH") / 4

    @property
    def intersection(self):
        return self._road.intersections[self._id]

    @property
    def direction(self):
        if self._id:
            return (self._road.start - self._road.end).normalize()
        else:
            return (self._road.end - self._road.start).normalize()
    
    def contains(self, position):
        return _dist(*(tuple(self.start) + tuple(self.end) + tuple(position))) < get_env("ROAD_WIDTH")


class RoadModel:
    def __init__(self, start: list, end: list, models: Models):
        self._start = start
        self._end = end
        self._model = models.add(f'{get_env("MODELS_DIR")}/roads/road',
                                 position=self._get_middle(),
                                 size=get_env('ROAD_WIDTH'))

    def _get_middle(self):
        return (self._start[0] - self._end[0]) // 2, \
               (self._start[1] - self._end[1]) // 2
