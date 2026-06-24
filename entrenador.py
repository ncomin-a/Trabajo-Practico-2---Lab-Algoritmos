import json
import random

from pokemon import Pokemon


GIMNASIOS = [
    {"numero": 1, "lider": "Brock",    "medalla": "Medalla Roca"},
    {"numero": 2, "lider": "Misty",    "medalla": "Medalla Cascada"},
    {"numero": 3, "lider": "Lt. Surge", "medalla": "Medalla Trueno"},
    {"numero": 4, "lider": "Erika",    "medalla": "Medalla Arcoiris"},
    {"numero": 5, "lider": "Koga",     "medalla": "Medalla Veneno"},
    {"numero": 6, "lider": "Sabrina",  "medalla": "Medalla Marsh"},
    {"numero": 7, "lider": "Blaine",   "medalla": "Medalla Volcán"},
    {"numero": 8, "lider": "Giovanni", "medalla": "Medalla Tierra"},
]


class Entrenador:
    MAX_EQUIPO = 6
    MAX_PILA_TRANSFERENCIAS = 5

    def __init__(self, nombre="Entrenador"):
        self.nombre = nombre