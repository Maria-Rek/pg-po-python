from organisms.plant import Plant
from organisms.animal import Animal
from organisms.animals.cybersheep import CyberSheep
from utils.point import Point
from utils.direction import Direction
from PIL import Image

class Hogweed(Plant):
    def __init__(self, position: Point):
        super().__init__(position, strength=10)

    def name(self) -> str:
        return "Hogweed"

    def action(self, world):
        for direction in Direction:
            if direction == Direction.NONE:
                continue
            neighbor = direction.step(self._position)
            if not world.is_inside_board(neighbor):
                continue

            target = world.get_organism_at(neighbor)
            if target and isinstance(target, Animal) and not isinstance(target, CyberSheep):
                world.add_log(f"{self.name()} killed {target.name()} next to it")
                world.remove_organism(target)

        super().action(world)  # may still spread

    def collision(self, other, world):
        if isinstance(other, CyberSheep):
            world.add_log(f"{other.name()} ate {self.name()} and survived!")
        else:
            world.add_log(f"{other.name()} ate {self.name()} and died!")
            world.remove_organism(other)
        world.remove_organism(self)

    def get_image(self):
        try:
            return Image.open("resources/hogweed.png")
        except:
            return None
