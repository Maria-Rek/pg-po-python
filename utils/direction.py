from enum import Enum
from utils.point import Point

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)
    NONE = (0, 0)

    def step(self, start: Point) -> Point:
        dx, dy = self.value
        return Point(start.get_x() + dx, start.get_y() + dy)
