import tkinter as tk
from tkinter import simpledialog, messagebox, Label, Entry, Button, Toplevel
from gui.view import View
from world.world import World
from organisms.organism_factory import get_class_by_name
from organisms.animals.human import Human
from utils.point import Point
import random

class Game:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.root.iconphoto(False, tk.PhotoImage(file="resources/logo.png"))
        self.root.title("Maria Rek 203174")
        self.root.configure(bg="#f0d0f5")

        self.view = None
        self.world = None
        self.max_turns = 0
        self.info_label = None

        self._start_game_dialog()
        self.root.mainloop()

    def _setup_controls(self):
        self.control_frame = tk.Frame(self.root, bg="#f0d0f5")
        self.control_frame.pack()

        tk.Button(self.control_frame, text="Next Turn", command=self._next_turn).grid(row=0, column=0, padx=5)
        tk.Button(self.control_frame, text="Save", command=self._save_game).grid(row=0, column=1, padx=5)
        tk.Button(self.control_frame, text="Load", command=self._load_game).grid(row=0, column=2, padx=5)
        tk.Button(self.control_frame, text="New Game", command=self._start_game_dialog).grid(row=0, column=3, padx=5)

        self.log_area = tk.Text(self.root, height=8, width=60, bg="#fff0fb")
        self.log_area.pack()

    def _start_game_dialog(self):
        option = messagebox.askyesno("Start", "Do you want to load a saved game?")
        if option:
            self._load_game()
        else:
            self._new_game()

    def _new_game(self):
        dialog = Toplevel(self.root)
        dialog.title("New Game Setup")
        dialog.geometry("250x160")
        dialog.configure(bg="#f0d0f5")
        dialog.grab_set()

        Label(dialog, text="Width:", bg="#f0d0f5").pack()
        width_entry = Entry(dialog)
        width_entry.insert(0, "10")
        width_entry.pack()

        Label(dialog, text="Height:", bg="#f0d0f5").pack()
        height_entry = Entry(dialog)
        height_entry.insert(0, "10")
        height_entry.pack()

        Label(dialog, text="Turns:", bg="#f0d0f5").pack()
        turns_entry = Entry(dialog)
        turns_entry.insert(0, "10")
        turns_entry.pack()

        def confirm():
            try:
                w = int(width_entry.get())
                h = int(height_entry.get())
                t = int(turns_entry.get())
                if w <= 0 or h <= 0 or t <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Error", "Invalid input")
                dialog.destroy()
                return

            self.world = World(w, h)
            self.max_turns = t
            self.world.set_max_turns(t)
            dialog.destroy()
            self._choose_add_method()

        Button(dialog, text="Start Game", command=confirm).pack(pady=10)

    def _choose_add_method(self):
        method = messagebox.askyesno("Add organisms", "Add organisms randomly?\n(Yes = random, No = manually)")
        if method:
            self._add_random_organisms()
        self._start_view()

    def _add_random_organisms(self):
        width = self.world.get_width()
        height = self.world.get_height()
        total_fields = width * height
        count = random.randint(int(total_fields * 0.2), int(total_fields * 0.35))

        all_positions = [Point(x, y) for x in range(width) for y in range(height)]
        random.shuffle(all_positions)

        # Add Human first
        pos = all_positions.pop()
        human = Human(pos)
        self.world.add_organism(human)

        for _ in range(count - 1):
            if not all_positions:
                break
            pos = all_positions.pop()
            klass = random.choice([
                "Sheep", "Wolf", "Fox", "Turtle", "Antelope", "CyberSheep",
                "Grass", "Dandelion", "Guarana", "DeadlyNightshade", "Hogweed"
            ])
            cls = get_class_by_name(klass)
            if cls:
                self.world.add_organism(cls(pos))

        self.world.add_log(f"Randomly added {count} organisms (including Human)")

    def _load_game(self):
        name = simpledialog.askstring("Load", "Enter save file name:")
        if not name:
            return
        loaded = World.load_from_file(name + ".txt")
        if loaded:
            self.world = loaded
            self.max_turns = self.world.get_max_turns()
            self._start_view()
        else:
            messagebox.showerror("Load failed", f"Couldn't load {name}.txt")

    def _save_game(self):
        if not self.world:
            return
        name = simpledialog.askstring("Save", "Enter file name to save:")
        if name:
            self.world.save_to_file(name + ".txt")
            self._log("Game saved!")

    def _start_view(self):
        self.root.deiconify()
        self._setup_controls()

        if self.view:
            self.view.destroy()
        if self.info_label:
            self.info_label.destroy()

        self.info_label = tk.Label(self.root, text="Welcome to Virtual World!", font=("Cascadia Code", 12), bg="#f0d0f5")
        self.info_label.pack(pady=10)

        self.view = View(self.root, self.world, self.info_label, self.max_turns)
        self.view.pack()
        self.root.bind("<Key>", self.view.on_key)
        self._refresh_logs()

    def _next_turn(self):
        if self.world.get_turn() >= self.max_turns:
            self._log("Game over")
            self._end_game_dialog()
            return

        self.view.execute_turn()

        if self.world.get_turn() >= self.max_turns:
            self._log("Max turns reached!")
            self._end_game_dialog()

        self._refresh_logs()

    def _end_game_dialog(self):
        dialog = Toplevel(self.root)
        dialog.title("Game Over")
        dialog.geometry("300x150")
        dialog.configure(bg="#f0d0f5")
        dialog.grab_set()

        Label(dialog, text="Game over! What do you want to do?", bg="#f0d0f5", font=("Cascadia Code", 11)).pack(pady=10)

        Button(dialog, text="New Game", width=20, command=lambda: [dialog.destroy(), self._new_game()]).pack(pady=5)
        Button(dialog, text="Load Game", width=20, command=lambda: [dialog.destroy(), self._load_game()]).pack(pady=5)
        Button(dialog, text="Exit", width=20, command=self.root.destroy).pack(pady=5)

    def _refresh_logs(self):
        self.log_area.delete("1.0", tk.END)
        logs = self.world.flush_logs()
        for line in logs:
            self.log_area.insert(tk.END, line + "\n")

    def _log(self, text):
        self.world.add_log(text)
        self._refresh_logs()
