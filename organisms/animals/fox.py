from organisms.animal import Animal
from utils.point import Point
from PIL import Image
import random

class Fox(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=3, initiative=7)

    def name(self) -> str:
        return "Fox"

    def action(self, world):
        safe_moves = []
        for pos in world.get_adjacent_positions(self._position):
            target = world.get_organism_at(pos)
            if target is None or target.get_strength() <= self._strength:
                safe_moves.append(pos)

        if safe_moves:
            new_position = random.choice(safe_moves)  # <== poprawka tu
            target = world.get_organism_at(new_position)
            if target:
                self.collision(target, world)
            else:
                self.set_position(new_position)
        else:
            world.add_log(f"{self.name()} found no safe move and stayed in place")

        self.increase_age()

    def get_image(self):
        try:
            return Image.open("resources/fox.png")
        except:
            return None
