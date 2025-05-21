from organisms.animal import Animal
from utils.point import Point
from utils.direction import Direction
from PIL import Image

class Human(Animal):
    def __init__(self, position: Point):
        super().__init__(position, strength=5, initiative=4)
        self._special_active = False
        self._special_turns_left = 0
        self._cooldown = 0
        self._pending_activation = False
        self._planned_move = Direction.NONE

    def name(self) -> str:
        return "Human"

    def plan_move(self, direction: Direction):
        self._planned_move = direction

    def activate_special(self):
        if not self._special_active and self._cooldown == 0 and not self._pending_activation:
            self._pending_activation = True
            return "Preparing to activate Firestorm 🔥"
        return "Cannot activate yet."

    def action(self, world):
        if self._planned_move != Direction.NONE:
            target = self._planned_move.step(self._position)
            if world.is_inside_board(target):
                target_organism = world.get_organism_at(target)
                if target_organism:
                    self.collision(target_organism, world)
                else:
                    self.set_position(target)
            else:
                world.add_log("Human tried to leave the map!")
        self._planned_move = Direction.NONE

        if self._pending_activation:
            self._special_active = True
            self._special_turns_left = 5
            self._pending_activation = False
            world.add_log("Human activated Firestorm 🔥 (5 turns)")

        if self._special_active:
            for direction in Direction:
                if direction == Direction.NONE:
                    continue
                neighbor = direction.step(self._position)
                if world.is_inside_board(neighbor):
                    target = world.get_organism_at(neighbor)
                    if target and target != self:
                        world.add_log(f"{target.name()} was burned by Human 🔥")
                        world.remove_organism(target)
            self._special_turns_left -= 1
            if self._special_turns_left == 0:
                self._special_active = False
                self._cooldown = 5
                world.add_log("Human's Firestorm ended. Cooldown: 5 turns.")
        elif self._cooldown > 0:
            self._cooldown -= 1

        self.increase_age()

    def collision(self, other, world):
        if other is None:
            return
        super().collision(other, world)

    def get_cooldown(self) -> int:
        return self._cooldown

    def get_special_turns_left(self) -> int:
        return self._special_turns_left

    def is_special_active(self) -> bool:
        return self._special_active

    def get_status_text(self) -> str:
        if self._special_active:
            return f"ACTIVE ({self._special_turns_left}/5) 🔥"
        elif self._pending_activation:
            return "Starting soon ⏳"
        elif self._cooldown > 0:
            return f"Cooldown ({self._cooldown}/5)"
        else:
            return "Ready"

    def get_image(self):
        try:
            return Image.open("resources/human.png")
        except:
            return None
