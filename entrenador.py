import json
import random

from pokemon import Pokemon
from estructuras import ListaEnlazada


GIMNASIOS = [
    {"numero": 1, "lider": "Brock",     "medalla": "Medalla Roca"},
    {"numero": 2, "lider": "Misty",     "medalla": "Medalla Cascada"},
    {"numero": 3, "lider": "Lt. Surge", "medalla": "Medalla Trueno"},
    {"numero": 4, "lider": "Erika",     "medalla": "Medalla Arcoiris"},
    {"numero": 5, "lider": "Koga",      "medalla": "Medalla Veneno"},
    {"numero": 6, "lider": "Sabrina",   "medalla": "Medalla Marsh"},
    {"numero": 7, "lider": "Blaine",    "medalla": "Medalla Volcán"},
    {"numero": 8, "lider": "Giovanni",  "medalla": "Medalla Tierra"},
]


class Entrenador:
    MAX_EQUIPO = 6
    MAX_PILA_TRANSFERENCIAS = 5

    def __init__(self, nombre="Entrenador"):
        self.nombre = nombre

        self.pokedex = {}

        self.equipo_principal = []

        self.pc = ListaEnlazada()

        self.medallas = set()

        self.pila_transferencias = ListaEnlazada()

        self.cola_centro_pokemon = ListaEnlazada()

    def cargar_pokedex_desde_json(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        cantidad = 0
        for entrada in datos.get("pokemons", []):
            pokemon = Pokemon(id_pokemon = entrada["id"], nombre = entrada["nombre"], tipo = entrada["tipo"], poder_combate = entrada["poder_combate"])
            self.pokedex[pokemon.id] = pokemon

            if len(self.equipo_principal) < self.MAX_EQUIPO:
                self.equipo_principal.append(pokemon)
            else:
                self.pc.append(pokemon)

            cantidad += 1
        return cantidad

    def cargar_medallas_desde_json(self, ruta_archivo, cantidad_a_precargar=2):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        cargadas = 0
        for medalla in datos.get("medallas", []):
            if cargadas >= cantidad_a_precargar:
                break
            if isinstance(medalla, dict):
                nombre = medalla.get("nombre")
            else:
                nombre = medalla
            self.medallas.add(nombre)
            cargadas += 1
        return cargadas

    def agregar_medalla(self, nombre_medalla):
        if nombre_medalla in self.medallas:
            print(f"Ya tenés la {nombre_medalla}, no se puede duplicar.")
            return False
        self.medallas.add(nombre_medalla)
        print(f"  {self.nombre} obtuvo la {nombre_medalla}!")
        return True

    def generar_pokemon_aleatorio(self):
        pass

    def capturar_pokemon(self, pokemon):
        pokemon = 

        capturado = random.choice([True, False])
        if capturado:
            print(f"{self.nombre} atrapó un {pokemon}!")
            self.agregar_medalla(medalla)
        else:
            print(f"{self.nombre} no pudo atrapar a {pokemon}. Segui intentando!")

        return capturado

    def atender_centro_pokemon(self):
        if self.cola_centro_pokemon.esta_vacia():
            print("No hay Pokemon esperando en el Centro.")
            return
        print("Enfermera Joy: Curando a tus Pokemon...")
        while not self.cola_centro_pokemon.esta_vacia():
            pokemon = self.cola_centro_pokemon.pop_front()
            pokemon.sanar()
            print(f"  {pokemon.nombre} -> sanado.")
        print("Enfermera Joy: Tus Pokemon estan listos!")

    def transferir_a_oak(self, pokemon):
        if not self.pc.remove_dato(pokemon):
            print(f"{pokemon.nombre} no estaba en la PC.")
            return

        if len(self.pila_transferencias) >= self.MAX_PILA_TRANSFERENCIAS:
            self.pila_transferencias.pop_back()

        self.pila_transferencias.push_front(pokemon)
        print(f"{pokemon.nombre} fue transferido al Profesor Oak.")

    def deshacer_transferencia(self):
        if self.pila_transferencias.esta_vacia():
            print("No hay transferencias para deshacer.")
            return
        pokemon = self.pila_transferencias.pop_front()
        self.pc.append(pokemon)
        print(f"{pokemon.nombre} volvió a la PC.")

    def busqueda_lineal_equipo(self, nombre):
        nombre = nombre.lower()
        for pokemon in self.equipo_principal:
            if pokemon.nombre.lower() == nombre:
                return pokemon
        return None

    def busqueda_binaria_pokedex(self, id_buscado):
        ids_ordenados = sorted(self.pokedex.keys())
        izq = 0
        der = len(ids_ordenados) - 1

        while izq <= der:
            medio = (izq + der) // 2
            if ids_ordenados[medio] == id_buscado:
                return self.pokedex[id_buscado]
            elif ids_ordenados[medio] < id_buscado:
                izq = medio + 1
            else:
                der = medio - 1

        return None 

    def desafiar_gimnasio(self, gimnasio):
        lider = gimnasio["lider"]
        medalla = gimnasio["medalla"]
        print(f"{self.nombre} desafía al Lider {lider}...")

        gano = random.choice([True, False])
        if gano:
            print(f"  {self.nombre} derrotó a {lider}!")
            self.agregar_medalla(medalla)
        else:
            print(f"  {self.nombre} perdió contra {lider}. Seguí entrenando!")

        return gano