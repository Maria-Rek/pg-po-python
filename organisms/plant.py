from abc import ABC
from organisms.organism import Organism
from utils.point import Point
import random

class Plant(Organism, ABC):
    def __init__(self, position: Point, strength: int):
        super().__init__(position, strength, 0)

    def action(self, world):
        if random.randint(0, 9) == 0:  # 10% chance to spread
            free = world.get_free_adjacent_positions(self._position)
            if free:
                new_pos = random.choice(free)
                world.create_organism(type(self), new_pos)
                world.add_log(f"{self.name()} spread")
        self.increase_age()

    def collision(self, other, world):
        if other is None:
            return

        if self.name() in ["Grass", "Dandelion"]:  # special case
            if other.__class__.__name__ == "Sheep":
                world.add_log(f"{self.name()} was eaten by Sheep")
                world.remove_organism(self)
            else:
                world.add_log(f"{other.name()} stepped on {self.name()}")
                other.set_position(self._position)
            return

        world.add_log(f"{self.name()} was eaten by {other.name()}")
        world.remove_organism(self)
        other.set_position(self._position)
