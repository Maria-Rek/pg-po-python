# Virtual World (Python)

GUI-based 2D world simulator where organisms live, move, fight, and reproduce according to individual behavior rules.

The game is turn-based. Organisms act based on initiative and age, with the board and event logs displayed in a Tkinter-based GUI.  
Game state can be saved and loaded from a text file.

---

## Core Concepts

- `World` class managing the board and simulation flow
- Abstract `Organism` base class
- `Animal` and `Plant` hierarchies
- Polymorphism and encapsulation
- Turn order determined by initiative and age
- Collision handling and same-species reproduction
- 8-neighborhood movement model
- Tkinter-based GUI with PNG icon rendering
- Text-based save/load system

---

## Organisms

### Animals
- Wolf
- Sheep
- Fox (avoids stronger organisms)
- Turtle (25% move chance, blocks weaker attacks)
- Antelope (extended movement, 50% escape chance)
- CyberSheep (actively hunts Hogweed)

### Plants
- Grass
- Dandelion (multiple spread attempts)
- Guarana (increases strength)
- Deadly Nightshade (poisonous)
- Hogweed (damages surrounding organisms except CyberSheep)

### Human
- Controlled via arrow keys
- Special ability: **Firestorm**
  - 5 turns active
  - 5 turns cooldown
  - Activated with spacebar

---

## Project Structure

- `gui/` – main window and board rendering
- `world/` – world logic
- `organisms/` – organism hierarchy (`animals/`, `plants/`)
- `utils/` – helper classes
- `resources/` – PNG icons
- `save/` – saved game files

---

Project for the *Object-Oriented Programming* course (2024/2025) at Gdańsk University of Technology.
