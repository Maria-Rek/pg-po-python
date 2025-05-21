from organisms.organism import Organism
from organisms.animals.human import Human
from utils.point import Point
import os

class SquareWorld:
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

    def find_organism(self, point: Point) -> Organism | None:
        for org in self._organisms:
            if org.get_position() == point:
                return org
        return None

    def add_organism(self, organism: Organism):
        self._organisms.append(organism)

    def remove_organism(self, organism: Organism):
        if organism in self._organisms:
            self._organisms.remove(organism)

    def get_all_organisms(self) -> list[Organism]:
        return self._organisms

    def add_log(self, message: str):
        self._logs.append(message)

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

    def save_to_file(self, filename: str):
        os.makedirs("save", exist_ok=True)
        filepath = os.path.join("save", filename)
        with open(filepath, "w") as file:
            file.write(f"SIZE {self._width} {self._height}\n")
            file.write(f"TURN {self._turn}\n")
            file.write(f"MAX_TURNS {self._max_turns}\n")
            for org in self._organisms:
                pos = org.get_position()
                if isinstance(org, Human):
                    file.write(f"Human {pos.get_x()} {pos.get_y()} {org.get_age()} {org.get_cooldown()} {org.get_special_turns_left()} {org.is_special_active()}\n")
                else:
                    file.write(f"{org.name()} {pos.get_x()} {pos.get_y()} {org.get_age()}\n")

    @staticmethod
    def load_from_file(filename: str):
        from global_world import GlobalWorld
        from organisms.animals.human import Human
        from organisms import organism_factory  # needs factory method

        filepath = os.path.join("save", filename)
        if not os.path.isfile(filepath):
            GlobalWorld.add_log(f"File not found: {filepath}")
            return None

        with open(filepath, "r") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        size_line = lines.pop(0).split()
        width, height = int(size_line[1]), int(size_line[2])
        world = SquareWorld(width, height)

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

        GlobalWorld.add_log(f"Game loaded from {filepath}")
        return world
