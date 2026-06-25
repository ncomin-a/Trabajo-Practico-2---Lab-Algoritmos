import json
import random

from pokemon import Pokemon
from estructuras import ListaEnlazada


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

        # Catálogo global local del entrenador: id -> Pokemon
        self.pokedex = {}

        # Equipo principal como lista Python (máx. 6)
        self.equipo_principal = []

        # PC como ListaEnlazada (sin límite)
        self.pc = ListaEnlazada()

        # Medallas como conjunto para evitar duplicados
        self.medallas = set()

        # Pila para las últimas transferencias (comportamiento tipo stack/deque)
        self.pila_transferencias = ListaEnlazada()

        # Cola para el Centro Pokémon
        self.cola_centro_pokemon = ListaEnlazada()

    def cargar_pokedex_desde_json(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as cargar:
            datos = json.load(cargar)

        cantidad_cargados = 0
        for entrada in datos.get("pokemons", []):
            pokemon = Pokemon(
                id_pokemon=entrada["id"],
                nombre=entrada["nombre"],
                tipo=entrada["tipo"],
                poder_combate=entrada["poder_combate"],
            )
            self.pokedex[pokemon.id] = pokemon
            if len(self.equipo_principal) < self.MAX_EQUIPO:
                self.equipo_principal.append(pokemon)
            else:
                self.pc.append(pokemon)
            cantidad_cargados += 1

        return cantidad_cargados

    def cargar_medallas_desde_json(self, ruta_archivo):
        with open(ruta_archivo, "r", encoding="utf-8") as cargar:
            datos = json.load(cargar)

        cantidad_cargadas = 0
        for medalla in datos.get("medallas", []):
            # Guardar sólo el nombre de la medalla para el conjunto
            nombre = medalla.get("nombre") if isinstance(medalla, dict) else medalla
            if nombre not in self.medallas:
                self.medallas.add(nombre)
                cantidad_cargadas += 1

        return cantidad_cargadas

    def agregar_medalla(self, medalla):
        nombre_medalla = medalla.get("nombre", medalla) if isinstance(medalla, dict) else medalla
        if nombre_medalla in self.medallas:
            print(f"{self.nombre} ya posee la {nombre_medalla}.")
            return False
        self.medallas.add(nombre_medalla)
        print(f"{self.nombre} ha obtenido la {nombre_medalla}.")
        return True

    def generar_pokemon_aleatorio(self):
        nombre = f"Pokémon {random.randint(1, 100)}"
        nivel = random.randint(1, 100)
        tipo = random.choice(["Fuego", "Agua", "Planta", "Eléctrico", "Psíquico", "Normal"])
        poder_combate = random.randint(50, 100)
        hp = random.randint(50, 100)
        id_pokemon = random.randint(1, 100)
        return Pokemon(id_pokemon=id_pokemon, nombre=nombre, tipo=tipo, poder_combate=poder_combate, hp=hp, nivel=nivel)

    def capturar_pokemon(self, pokemon):
        self.pokedex[pokemon.id] = pokemon
        if len(self.equipo_principal) < self.MAX_EQUIPO:
            self.equipo_principal.append(pokemon)
            print(f"{self.nombre} ha capturado a {pokemon.nombre} y se unió al equipo principal.")
        else:
            self.pc.append(pokemon)
            print(f"{self.nombre} ha capturado a {pokemon.nombre}. El equipo está lleno, fue enviado al PC.")

    def enviar_pokemon_centro(self, pokemon):
        if pokemon in self.equipo_principal:
            self.cola_centro_pokemon.append(pokemon)
            print(f"{pokemon.nombre} fue enviado al Centro Pokémon y espera turno para ser sanado.")
        else:
            print(f"{pokemon.nombre} no está en el equipo de {self.nombre}.")

    def atender_siguiente_en_centro(self):
        if self.cola_centro_pokemon.esta_vacia():
            print("No hay Pokémon esperando en el Centro Pokémon.")
            return None
        pokemon = self.cola_centro_pokemon.pop_front()
        pokemon.sanar()
        print(f"{pokemon.nombre} ha sido sanado en el Centro Pokémon.")
        return pokemon

    def sanar_pokemon(self, pokemon):
        if pokemon in self.equipo_principal:
            pokemon.sanar()
            print(f"{pokemon.nombre} ha sido sanado.")
        else:
            print(f"{pokemon.nombre} no está en el equipo de {self.nombre}.")

    def transferir_pokemon(self, pokemon, otro_entrenador):
        if pokemon not in self.equipo_principal:
            print(f"{pokemon.nombre} no está en el equipo de {self.nombre}.")
            return

        if len(otro_entrenador.equipo_principal) >= otro_entrenador.MAX_EQUIPO:
            print(f"{otro_entrenador.nombre} no puede recibir más Pokémon. El equipo está lleno.")
            return

        self.equipo_principal.remove(pokemon)
        otro_entrenador.equipo_principal.append(pokemon)

        if len(self.pila_transferencias) >= self.MAX_PILA_TRANSFERENCIAS:
            self.pila_transferencias.pop_back()
        self.pila_transferencias.push_front((pokemon, self, otro_entrenador))

        print(f"{self.nombre} ha transferido a {pokemon.nombre} a {otro_entrenador.nombre}.")

    def deshacer_transferencia(self):
        if self.pila_transferencias.esta_vacia():
            print(f"{self.nombre} no tiene transferencias para deshacer.")
            return

        pokemon, origen, destino = self.pila_transferencias.pop_front()

        if pokemon not in destino.equipo_principal:
            print(f"No se puede deshacer: {pokemon.nombre} ya no está en el equipo de {destino.nombre}.")
            return

        if len(origen.equipo_principal) >= origen.MAX_EQUIPO:
            print(f"No se puede deshacer: el equipo de {origen.nombre} está lleno.")
            return

        destino.equipo_principal.remove(pokemon)
        origen.equipo_principal.append(pokemon)
        print(f"Se deshizo la transferencia: {pokemon.nombre} volvió de {destino.nombre} a {origen.nombre}.")

    def consultar_pokemon_por_id(self, id_pokemon):
        return self.pokedex.get(id_pokemon)

    def desafiar_gimnasio(self, gimnasio):
        if gimnasio in GIMNASIOS:
            print(f"{self.nombre} desafía al líder {gimnasio['lider']} del gimnasio {gimnasio['numero']}.")
        else:
            print(f"El gimnasio {gimnasio} no existe.")