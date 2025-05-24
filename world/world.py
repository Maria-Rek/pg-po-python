from typing import Optional, Type
from organisms.organism import Organism
from organisms.animals.human import Human
from utils.point import Point
from utils.direction import Direction
import random
import os

class World:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._organisms: list[Organism] = []
        self._logs: list[str] = []
        self._turn = 0
        self._max_turns = 0

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def is_occupied(self, point: Point) -> bool:
        return self.find_organism(point) is not None

    def find_organism(self, point: Point) -> Optional[Organism]:
        for org in self._organisms:
            if org.get_position() == point:
                return org
        return None

    def get_organism_at(self, point: Point) -> Optional[Organism]:
        return self.find_organism(point)

    def add_organism(self, organism: Organism):
        self._organisms.append(organism)

    def remove_organism(self, organism: Organism):
        if organism in self._organisms:
            self._organisms.remove(organism)

    def get_all_organisms(self) -> list[Organism]:
        return self._organisms

    def add_log(self, message: str):
        self._logs.append(message)
        print(self.color_log(message))

    def flush_logs(self) -> list[str]:
        logs = self._logs[:]
        self._logs.clear()
        return logs

    def get_turn(self) -> int:
        return self._turn

    def increase_turn(self):
        self._turn += 1

    def set_max_turns(self, value: int):
        self._max_turns = value

    def get_max_turns(self) -> int:
        return self._max_turns

    def is_inside_board(self, point: Point) -> bool:
        return 0 <= point.get_x() < self._width and 0 <= point.get_y() < self._height

    def get_adjacent_positions(self, center: Point) -> list[Point]:
        result = []
        for d in Direction:
            if d == Direction.NONE:
                continue
            p = d.step(center)
            if self.is_inside_board(p):
                result.append(p)
        return result

    def get_free_adjacent_positions(self, center: Point) -> list[Point]:
        positions = self.get_adjacent_positions(center)
        return [p for p in positions if not self.is_occupied(p)]

    def create_organism(self, organism_class: Type[Organism], position: Point):
        try:
            instance = organism_class(position)
            self.add_organism(instance)
        except Exception as e:
            self.add_log(f"Error creating {organism_class.__name__}: {e}")

    def find_nearest(self, name: str, from_pos: Point) -> Optional[Organism]:
        min_dist = float('inf')
        closest = None
        for org in self._organisms:
            if org.name() == name:
                dist = abs(org.get_position().get_x() - from_pos.get_x()) + abs(org.get_position().get_y() - from_pos.get_y())
                if dist < min_dist:
                    min_dist = dist
                    closest = org
        return closest

    def move_towards(self, start: Point, goal: Point) -> Point:
        dx = goal.get_x() - start.get_x()
        dy = goal.get_y() - start.get_y()
        step_x = 1 if dx > 0 else -1 if dx < 0 else 0
        step_y = 1 if dy > 0 else -1 if dy < 0 else 0
        target = Point(start.get_x() + step_x, start.get_y() + step_y)
        return target if self.is_inside_board(target) else start

    def color_log(self, text: str) -> str:
        lower = text.lower()
        if any(kw in lower for kw in ["killed", "died", "eaten", "burned"]):
            return f"\033[91m{text}\033[0m"
        elif "spread" in lower:
            return f"\033[92m{text}\033[0m"
        elif "reproduced" in lower:
            return f"\033[93m{text}\033[0m"
        elif "firestorm" in lower:
            return f"\033[95m{text}\033[0m"
        else:
            return f"\033[95m{text}\033[0m"

    @staticmethod
    def load_from_file(filename: str):
        from organisms import organism_factory

        filepath = os.path.join("save", filename)
        if not os.path.isfile(filepath):
            print(f"File not found: {filepath}")
            return None

        with open(filepath, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        size_line = lines.pop(0).split()
        width, height = int(size_line[1]), int(size_line[2])
        world = World(width, height)

        turn_line = lines.pop(0).split()
        world._turn = int(turn_line[1])

        max_turns_line = lines.pop(0).split()
        world._max_turns = int(max_turns_line[1])

        for line in lines:
            tokens = line.split()
            name = tokens[0]
            x, y = int(tokens[1]), int(tokens[2])
            age = int(tokens[3])
            pos = Point(x, y)

            if name == "Human":
                cooldown = int(tokens[4])
                active_turns = int(tokens[5])
                active = tokens[6].lower() == "true"
                h = Human(pos)
                h.set_age(age)
                h._cooldown = cooldown
                h._special_turns_left = active_turns
                h._special_active = active
                world.add_organism(h)
            else:
                org_class = organism_factory.get_class_by_name(name)
                if org_class:
                    org = org_class(pos)
                    org.set_age(age)
                    world.add_organism(org)

        print(f"Game loaded from {filepath}")
        return world
