import tkinter as tk
from tkinter import Menu
from PIL import ImageTk
from utils.direction import Direction
from organisms.animals.human import Human
from organisms.organism_factory import get_class_by_name
from utils.point import Point

class View(tk.Frame):
    def __init__(self, root, world, info_label, max_turns):
        super().__init__(root)
        self.cell_size = 50
        self.world = world
        self.info_label = info_label
        self.max_turns = max_turns
        self.image_cache = {}

        self.log_area = root.nametowidget('log_area') if 'log_area' in root.children else None

        canvas_width = world.get_width() * self.cell_size
        canvas_height = world.get_height() * self.cell_size

        # Canvas + scrollbary
        self.canvas = tk.Canvas(self, width=min(canvas_width, 700), height=min(canvas_height, 700),
                               bg="white", highlightthickness=0, scrollregion=(0,0,canvas_width,canvas_height))
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vbar.grid(row=0, column=1, sticky="ns")
        self.hbar.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.focus_set()

        self._draw_all()
        self._update_info()

    def _draw_all(self):
        self.canvas.delete("all")
        for x in range(self.world.get_width()):
            for y in range(self.world.get_height()):
                self.canvas.create_rectangle(
                    x * self.cell_size, y * self.cell_size,
                    (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                    outline="gray")

        plants = []
        animals = []
        for org in self.world.get_all_organisms():
            module = org.__class__.__module__.lower()
            if "plants" in module:
                plants.append(org)
            else:
                animals.append(org)

        for group in [plants, animals]:
            for org in group:
                pos = org.get_position()
                img = org.get_image()
                if img:
                    resized = img.resize((self.cell_size, self.cell_size))
                    photo = ImageTk.PhotoImage(resized)
                    self.image_cache[(pos.get_x(), pos.get_y())] = photo
                    self.canvas.create_image(
                        pos.get_x() * self.cell_size,
                        pos.get_y() * self.cell_size,
                        image=photo,
                        anchor=tk.NW)
        # Zawsze popraw region do scrollowania
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def _on_click(self, event):
        x = int(self.canvas.canvasx(event.x))
        y = int(self.canvas.canvasy(event.y))
        col = x // self.cell_size
        row = y // self.cell_size
        point = Point(col, row)

        if not self.world.is_inside_board(point):
            self._add_log("Clicked outside the board.", "info")
            self._refresh_logs()
            return

        if self.world.is_occupied(point):
            org = self.world.find_organism(point)
            self._add_log(f"{org.name()} at {point} | age: {org.get_age()} | str: {org.get_strength()}", "info")
            self._refresh_logs()
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
                self._add_log("Only one Human allowed!", "warn")
                self._refresh_logs()
                return

        klass = get_class_by_name(name)
        if klass:
            new_org = klass(point)
            self.world.add_organism(new_org)
            self._add_log(f"Added {name} at {point}", "info")
            self.image_cache.clear()
            self._draw_all()
            self._update_info()
            self._refresh_logs()

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
            self._add_log("No Human on board!", "warn")
            return

        if event.keysym in key_map:
            action = key_map[event.keysym]
            if action == "special":
                msg = human.activate_special()
                self._add_log(msg, "special")
            else:
                human.plan_move(action)
                self._add_log(f"Human plans move {action.name}", "move")

    def execute_turn(self):
        organisms = list(self.world.get_all_organisms())
        organisms.sort(key=lambda o: (o.get_initiative(), o.get_age()), reverse=True)

        for org in organisms:
            if org in self.world.get_all_organisms():
                org.action(self.world)

        self.world.increase_turn()
        self.image_cache.clear()
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

    def _add_log(self, text, typ="info"):
        if self.log_area is None:
            return
        self.world.add_log(text)
        self.log_area.config(state=tk.NORMAL)
        tag = self._color_tag_for_log(text, typ)
        self.log_area.insert(tk.END, text + "\n", tag)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def _refresh_logs(self):
        if self.log_area is None:
            return
        self.log_area.config(state=tk.NORMAL)
        self.log_area.delete("1.0", tk.END)
        logs = self.world.flush_logs()
        for line in logs:
            self.log_area.insert(tk.END, line + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def _color_tag_for_log(self, text, typ="info"):
        lower = text.lower()
        if "killed" in lower or "died" in lower or "burned" in lower or "eaten" in lower:
            tag = "dead"
        elif "spread" in lower:
            tag = "spread"
        elif "reproduced" in lower:
            tag = "move"
        elif "firestorm" in lower:
            tag = "special"
        elif "warn" in typ or "only one human" in lower:
            tag = "warn"
        elif "plans move" in lower:
            tag = "move"
        else:
            tag = typ

        if not self.log_area.tag_names():
            self.log_area.tag_config("dead", foreground="#d11b36", font=("Cascadia Code", 10, "bold"))
            self.log_area.tag_config("spread", foreground="#1c8538", font=("Cascadia Code", 10, "italic"))
            self.log_area.tag_config("move", foreground="#c07d0c", font=("Cascadia Code", 10))
            self.log_area.tag_config("special", foreground="#e156c9", font=("Cascadia Code", 10, "bold"))
            self.log_area.tag_config("info", foreground="#9844d3", font=("Cascadia Code", 10))
            self.log_area.tag_config("warn", foreground="#c21c1c", font=("Cascadia Code", 10, "bold"))
        return tag
