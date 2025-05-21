from organisms.plant import Plant
from utils.point import Point
from PIL import Image

class Grass(Plant):
    def __init__(self, position: Point):
        super().__init__(position, strength=0)

    def name(self) -> str:
        return "Grass"

    def get_image(self):
        try:
            return Image.open("resources/grass.png")
        except:
            return None
