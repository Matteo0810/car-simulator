from enum import Enum
from helpers.color import Color


class Weather(Enum):
    CLEAR = 1
    CLOUDY = 2
    RAIN = 3
    THUNDERSTORM = 4


class Time(Enum):
    DAY = "#74afe3"
    DUSK = "#cce79e"
    NIGHT = "#74afe3"
