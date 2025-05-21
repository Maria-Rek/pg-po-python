from typing import Optional, Type
from organisms.organism import Organism
from utils.point import Point
import random

class GlobalWorld:
    _world = None
    _logs = []

    @classmethod
    def set_world(cls, world):
        cls._world = world

    @classmethod
    def get_world(cls):
        return cls._world

    @classmethod
    def get_organism_at(cls, position: Point) -> Optional[Organism]:
        return cls._world.find_organism(position)

    @classmethod
    def remove_organism(cls, organism: Organism):
        cls._world.remove_organism(organism)

    @classmethod
    def add_organism(cls, organism: Organism):
        cls._world.add_organism(organism)

    @classmethod
    def create_organism(cls, organism_class: Type[Organism], position: Point):
        try:
            instance = organism_class(position)
            cls.add_organism(instance)
        except Exception as e:
            cls.add_log(f"Error creating {organism_class.__name__}: {e}")

    @classmethod
    def add_log(cls, text: str):
        cls._logs.append(text)
        print(cls.color_log(text))  # You can redirect to GUI later

    @classmethod
    def flush_logs(cls):
        logs = cls._logs.copy()
        cls._logs.clear()
        return logs

    @staticmethod
    def color_log(text: str) -> str:
        lower = text.lower()
        if any(kw in lower for kw in ["killed", "died", "eaten", "burned"]):
            return f"\033[91m{text}\033[0m"  # red
        elif "spread" in lower:
            return f"\033[92m{text}\033[0m"  # green
        elif "reproduced" in lower:
            return f"\033[93m{text}\033[0m"  # yellow
        elif "firestorm" in lower:
            return f"\033[95m{text}\033[0m"  # magenta
        else:
            return f"\033[95m{text}\033[0m"  # default = pink 💖

    @classmethod
    def get_adjacent_positions(cls, center: Point) -> list[Point]:
        from utils.direction import Direction
        result = []
        for d in Direction:
            if d == Direction.NONE:
                continue
            p = d.step(center)
            if cls._world.is_inside_board(p):
                result.append(p)
        return result

    @classmethod
    def get_free_adjacent_positions(cls, center: Point) -> list[Point]:
        positions = cls.get_adjacent_positions(center)
        return [p for p in positions if not cls._world.is_occupied(p)]

    @classmethod
    def find_nearest(cls, name: str, from_pos: Point) -> Optional[Organism]:
        min_dist = float('inf')
        closest = None
        for org in cls._world.get_all_organisms():
            if org.name() == name:
                dist = abs(org.get_position().get_x() - from_pos.get_x()) + abs(org.get_position().get_y() - from_pos.get_y())
                if dist < min_dist:
                    min_dist = dist
                    closest = org
        return closest

    @classmethod
    def move_towards(cls, start: Point, goal: Point) -> Point:
        dx = goal.get_x() - start.get_x()
        dy = goal.get_y() - start.get_y()
        step_x = 1 if dx > 0 else -1 if dx < 0 else 0
        step_y = 1 if dy > 0 else -1 if dy < 0 else 0
        target = Point(start.get_x() + step_x, start.get_y() + step_y)
        return target if cls._world.is_inside_board(target) else start
