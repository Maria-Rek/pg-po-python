from organisms.animal import Animal
from utils.point import Point
from PIL import Image
import random

class Turtle(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=2, initiative=1)

    def name(self) -> str:
        return "Turtle"

    def action(self, world):
        if random.random() < 0.25:
            super().action(world)
        else:
            world.add_log(f"{self.name()} didn't move (75% chance)")
            self.increase_age()

    def did_block_attack(self, attacker):
        return attacker.get_strength() < 5

    def get_image(self):
        try:
            return Image.open("resources/turtle.png")
        except:
            return None
