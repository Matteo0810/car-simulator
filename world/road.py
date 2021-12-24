from engine.scene.models import Models
from helpers.utils import *
from helpers.vector import Vector2
from helpers.dotenv import get_env


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


class RoadModel:

    def __init__(self, start, end, models: Models):
        self._start = start
        self._end = end
        self._coords = self._get_coords()
        self._length = self._get_length()
        self._model = models.add(f'{get_env("MODELS_DIR")}/roads/road')
        self._set()

    def _get_coords(self):
        xA, yA = self._start
        xB, yB = self._end
        width = get_env('ROAD_WIDTH')
        return [
            [xA, yA + width], [xA, yA - width],
            [xB, yB + width], [xB, yB + width]
        ]

    def _get_length(self):
        xA, yA, xB, yB = self._coords
        return [xA + xB, yA + yB]

    def _set(self):
        pass
