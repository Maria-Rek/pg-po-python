from organisms.plant import Plant
from utils.point import Point
from PIL import Image

class DeadlyNightshade(Plant):
    def __init__(self, position: Point):
        super().__init__(position, strength=99)

    def name(self) -> str:
        return "DeadlyNightshade"

    def collision(self, other, world):
        if other:
            world.add_log(f"{other.name()} ate {self.name()} and died!")
            world.remove_organism(other)
            world.remove_organism(self)

    def get_image(self):
        try:
            return Image.open("resources/deadly_nightshade.png")
        except:
            return None
