from organisms.animal import Animal
from utils.point import Point
from PIL import Image

class Sheep(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=4, initiative=4)

    def name(self) -> str:
        return "Sheep"

    def get_image(self):
        try:
            return Image.open("resources/sheep.png")
        except:
            return None
