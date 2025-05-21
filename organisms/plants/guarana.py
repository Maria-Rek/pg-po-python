from organisms.plant import Plant
from utils.point import Point
from PIL import Image

class Guarana(Plant):
    def __init__(self, position: Point):
        super().__init__(position, strength=0)

    def name(self) -> str:
        return "Guarana"

    def collision(self, other, world):
        if other:
            other.set_strength(other.get_strength() + 3)
            other.set_position(self._position)
            world.add_log(f"{self.name()} was eaten by {other.name()} (+3 strength)")
            world.remove_organism(self)

    def get_image(self):
        try:
            return Image.open("resources/guarana.png")
        except:
            return None
