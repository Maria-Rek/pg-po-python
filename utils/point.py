class Point:
    def __init__(self, x: int = 0, y: int = 0):
        self._x = x
        self._y = y

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def __eq__(self, other):
        return isinstance(other, Point) and self._x == other._x and self._y == other._y

    def __hash__(self):
        return hash((self._x, self._y))

    def __str__(self):
        return f"({self._x}, {self._y})"
