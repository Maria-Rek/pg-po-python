from organisms.animal import Animal
from utils.point import Point
from PIL import Image

class Wolf(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=9, initiative=5)

    def name(self) -> str:
        return "Wolf"

    def get_image(self):
        try:
            return Image.open("resources/wolf.png")
        except:
            return None
