from organisms.animal import Animal
from utils.point import Point
from PIL import Image


class CyberSheep(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=11, initiative=4)

    def name(self) -> str:
        return "CyberSheep"

    def action(self, world):
        target = world.find_nearest("Hogweed", self._position)

        if target:
            next_step = world.move_towards(self._position, target.get_position())
            occupant = world.get_organism_at(next_step)

            if occupant:
                self.collision(occupant, world)
            else:
                self.set_position(next_step)
        else:
            world.add_log(f"{self.name()} looked around but found no Hogweed")

        self.increase_age()

    def collision(self, other, world):
        if other.name() == "Hogweed":
            world.add_log(f"{other.name()} was killed by CyberSheep (immune to Hogweed)")
            world.remove_organism(other)
            self.set_position(other.get_position())
        else:
            super().collision(other, world)

    def get_image(self):
        try:
            return Image.open("resources/cybersheep.png")
        except:
            return None
