from organisms.plant import Plant
from utils.point import Point
from PIL import Image
import random

class Dandelion(Plant):
    def __init__(self, position: Point):
        super().__init__(position, strength=0)

    def name(self) -> str:
        return "Dandelion"

    def action(self, world):
        for _ in range(3):
            if random.randint(0, 9) == 0:
                free = world.get_free_adjacent_positions(self._position)
                if free:
                    new_pos = random.choice(free)
                    world.create_organism(Dandelion, new_pos)
                    world.add_log(f"{self.name()} spread")
        self.increase_age()

    def get_image(self):
        try:
            return Image.open("resources/dandelion.png")
        except:
            return None
