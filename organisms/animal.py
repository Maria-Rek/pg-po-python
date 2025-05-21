from abc import ABC
from organisms.organism import Organism
from utils.point import Point
from utils.direction import Direction
import random

class Animal(Organism, ABC):
    def __init__(self, position: Point, strength: int, initiative: int):
        super().__init__(position, strength, initiative)

    def action(self, world):
        adjacent = world.get_adjacent_positions(self._position)
        if adjacent:
            new_position = random.choice(adjacent)
            target = world.get_organism_at(new_position)

            if target is None:
                self.set_position(new_position)
            elif isinstance(target, Plant) and self.__class__.__name__ == "Sheep":
                self.set_position(new_position)
                target.collision(self, world)
            elif isinstance(target, Plant):
                self.set_position(new_position)
                world.add_log(f"{self.name()} stepped on {target.name()}")
            else:
                self.collision(target, world)

        self.increase_age()

    def collision(self, other, world):
        if other is None:
            return

        if isinstance(other, Plant):
            other.collision(self, world)
            return

        if other.did_block_attack(self):
            world.add_log(f"{other.name()} blocked the attack from {self.name()}")
            return

        if self.is_same_species(other) and self != other:
            free = world.get_free_adjacent_positions(self._position)
            if free:
                child_pos = random.choice(free)
                world.create_organism(type(self), child_pos)
                world.add_log(f"{self.name()} reproduced")
            return

        if self._strength >= other.get_strength():
            world.add_log(f"{other.name()} was killed by {self.name()}")
            world.remove_organism(other)
            self.set_position(other.get_position())
        else:
            world.add_log(f"{self.name()} was killed by {other.name()}")
            world.remove_organism(self)
