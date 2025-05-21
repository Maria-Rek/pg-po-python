import tkinter as tk
from tkinter import Menu
from PIL import ImageTk
from world.global_world import GlobalWorld
from utils.direction import Direction
from organisms.animals.human import Human
from organisms.organism import Organism
from organisms.organism_factory import get_class_by_name
from utils.point import Point

class View(tk.Canvas):
    def __init__(self, root, world, info_label, max_turns):
        width = world.get_width() * 50
        height = world.get_height() * 50
        super().__init__(root, width=width, height=height, bg="white", highlightthickness=0)

        self.world = world
        self.cell_size = 50
        self.info_label = info_label
        self.max_turns = max_turns
        self.bind("<Button-1>", self._on_click)
        self.image_cache = {}  # {Organism: ImageTk.PhotoImage}
        self.focus_set()
        self._draw_all()
        self._update_info()  # ← Dodajemy pierwszy raz od razu

    def _draw_all(self):
        self.delete("all")
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                self.create_rectangle(x * self.cell_size, y * self.cell_size,
                                      (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                      outline="gray")

        # sort: plants first, animals second
        organisms = sorted(self.world.get_all_organisms(), key=lambda o: isinstance(o, Organism))
        for org in organisms:
            pos = org.get_position()
            img = org.get_image()
            if img:
                if org not in self.image_cache:
                    self.image_cache[org] = ImageTk.PhotoImage(img.resize((self.cell_size, self.cell_size)))
                self.create_image(pos.get_x() * self.cell_size,
                                  pos.get_y() * self.cell_size,
                                  image=self.image_cache[org],
                                  anchor=tk.NW)

    def _on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        point = Point(col, row)

        if self.world.is_occupied(point):
            org = self.world.find_organism(point)
            GlobalWorld.add_log(f"{org.name()} at {point} | age: {org.get_age()} | str: {org.get_strength()}")
            return

        self._popup_add(point)

    def _popup_add(self, point: Point):
        menu = Menu(self, tearoff=0)

        for name in [
            "Sheep", "Wolf", "Fox", "Turtle", "Antelope", "CyberSheep", "Human",
            "Grass", "Dandelion", "Guarana", "DeadlyNightshade", "Hogweed"
        ]:
            menu.add_command(label=name, command=lambda n=name: self._add_organism(n, point))

        try:
            menu.tk_popup(self.winfo_pointerx(), self.winfo_pointery())
        finally:
            menu.grab_release()

    def _add_organism(self, name: str, point: Point):
        if name == "Human":
            if any(isinstance(o, Human) for o in self.world.get_all_organisms()):
                GlobalWorld.add_log("Only one Human allowed!")
                return

        klass = get_class_by_name(name)
        if klass:
            new_org = klass(point)
            self.world.add_organism(new_org)
            GlobalWorld.add_log(f"Added {name} at {point}")
            self._draw_all()
            self._update_info()

    def on_key(self, event):
        key_map = {
            "Up": Direction.UP,
            "Down": Direction.DOWN,
            "Left": Direction.LEFT,
            "Right": Direction.RIGHT,
            "space": "special"
        }
        human = next((o for o in self.world.get_all_organisms() if isinstance(o, Human)), None)
        if not human:
            GlobalWorld.add_log("No Human on board!")
            return

        if event.keysym in key_map:
            action = key_map[event.keysym]
            if action == "special":
                msg = human.activate_special()
                GlobalWorld.add_log(msg)
            else:
                human.plan_move(action)

    def execute_turn(self):
        organisms = list(self.world.get_all_organisms())  # snapshot
        organisms.sort(key=lambda o: (o.get_initiative(), o.get_age()), reverse=True)

        for org in organisms:
            if org in self.world.get_all_organisms():  # could have died
                org.action(self.world)

        self.world.increase_turn()
        self._draw_all()
        self._update_info()

    def _update_info(self):
        info = f"Turn: {self.world.get_turn()}/{self.max_turns} | Org: {len(self.world.get_all_organisms())}"
        human = next((o for o in self.world.get_all_organisms() if isinstance(o, Human)), None)
        if human:
            info += " | Human: " + human.get_status_text()
        else:
            info += " | Human dead"
        self.info_label.config(text="Welcome to Virtual World!\n" + info)
