from organisms.animal import Animal
from utils.point import Point
from PIL import Image
import random

class Antelope(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=4, initiative=4)

    def name(self) -> str:
        return "Antelope"

    def action(self, world):
        directions = world.get_movement_directions()
        extended_moves = []

        for d in directions:
            dx, dy = d.value
            new_x = self._position.get_x() + 2 * dx
            new_y = self._position.get_y() + 2 * dy
            new_pos = Point(new_x, new_y)

            if world.is_inside_board(new_pos):
                extended_moves.append(new_pos)

        if extended_moves:
            new_position = random.choice(extended_moves)
            target = world.get_organism_at(new_position)

            if target:
                self.collision(target, world)
            else:
                self.set_position(new_position)

        self.increase_age()

    def collision(self, other, world):
        if other is None:
            return

        if random.random() < 0.5:
            free = world.get_free_adjacent_positions(self._position)
            if free:
                escape_to = random.choice(free)
                self.set_position(escape_to)
                world.add_log(f"{self.name()} escaped from {other.name()}")
                return
            else:
                world.add_log(f"{self.name()} tried to escape but had no space")

        super().collision(other, world)

    def get_image(self):
        try:
            return Image.open("resources/antelope.png")
        except:
            return None
