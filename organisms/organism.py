from abc import ABC, abstractmethod
from utils.point import Point  # Zakładamy, że masz klasę Point (Punkt)

class Organism(ABC):
    def __init__(self, position: Point, strength: int, initiative: int):
        self._position = position
        self._strength = strength
        self._initiative = initiative
        self._age = 0

    @abstractmethod
    def action(self, world):
        """Defines organism behavior during a turn."""
        pass

    @abstractmethod
    def collision(self, other, world):
        """Defines organism behavior during a collision."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Returns the name of the organism."""
        pass

    @abstractmethod
    def get_image(self):
        """Returns the image/symbol for GUI representation."""
        pass

    def get_strength(self) -> int:
        return self._strength

    def set_strength(self, value: int):
        self._strength = value

    def get_initiative(self) -> int:
        return self._initiative

    def get_age(self) -> int:
        return self._age

    def set_age(self, value: int):
        self._age = value

    def increase_age(self):
        self._age += 1

    def get_position(self) -> Point:
        return self._position

    def set_position(self, point: Point):
        self._position = point

    def did_block_attack(self, attacker: 'Organism') -> bool:
        return False

    def is_same_species(self, other: 'Organism') -> bool:
        return type(self) == type(other)
