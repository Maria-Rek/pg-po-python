from organisms.animals.sheep import Sheep
from organisms.animals.wolf import Wolf
from organisms.animals.fox import Fox
from organisms.animals.turtle import Turtle
from organisms.animals.antelope import Antelope
from organisms.animals.cybersheep import CyberSheep
from organisms.animals.human import Human

from organisms.plants.grass import Grass
from organisms.plants.dandelion import Dandelion
from organisms.plants.guarana import Guarana
from organisms.plants.deadly_nightshade import DeadlyNightshade
from organisms.plants.hogweed import Hogweed

def get_class_by_name(name: str):
    mapping = {
        "Sheep": Sheep,
        "Wolf": Wolf,
        "Fox": Fox,
        "Turtle": Turtle,
        "Antelope": Antelope,
        "CyberSheep": CyberSheep,
        "Human": Human,

        "Grass": Grass,
        "Dandelion": Dandelion,
        "Guarana": Guarana,
        "DeadlyNightshade": DeadlyNightshade,
        "Hogweed": Hogweed,
    }
    return mapping.get(name)
