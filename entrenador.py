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

            cantidad += 1
        return cantidad

    def cargar_medallas_desde_json(self, ruta_archivo, cantidad_a_precargar=2):
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)

        cargadas = 0
        for medalla in datos.get("medallas", []):
            if cargadas >= cantidad_a_precargar:
                break
            nombre = medalla.get("nombre") if isinstance(medalla, dict) else medalla
            self.medallas.add(nombre)
            cargadas += 1
        return cargadas

    def agregar_medalla(self, nombre_medalla):
        if nombre_medalla in self.medallas:
            print(f"Ya tenés la {nombre_medalla}, no se puede duplicar")
            return False
        self.medallas.add(nombre_medalla)
        print(f"  ¡{self.nombre} obtuvo la {nombre_medalla}!")
        return True

    def generar_pokemon_aleatorio(self):
        id_aleatorio = random.choice(list(self.pokedex.keys()))
        return self.pokedex[id_aleatorio]

    def capturar_pokemon(self):
        pokemon = self.generar_pokemon_aleatorio()
        print(f"¡Apareció un {pokemon.nombre} salvaje! "
              f"(Tipo: {pokemon.tipo}, Poder de Combate: {pokemon.poder_combate})")

        capturado = random.choice([True, False])
        if not capturado:
            print(f"{pokemon.nombre} se escapó. ¡Seguí intentando!")
            return pokemon, False

        print(f"¡{self.nombre} atrapó a {pokemon.nombre}!")
        if len(self.equipo_principal) < self.MAX_EQUIPO:
            self.equipo_principal.append(pokemon)
            print(f"{pokemon.nombre} fue agregado al Equipo Principal ({len(self.equipo_principal)}/{self.MAX_EQUIPO})")
        else:
            self.pc.append(pokemon)
            print(f"El Equipo Principal está lleno (6/6). {pokemon.nombre} fue derivado automáticamente a la PC")

        return pokemon, True

    def enviar_pokemon_centro(self, pokemon):
        if pokemon in self.equipo_principal:
            self.equipo_principal.remove(pokemon)
        self.cola_centro_pokemon.append(pokemon)
        print(f"{pokemon.nombre} ingresó a la cola del Centro Pokémon")

    def atender_siguiente_en_centro(self):
        if self.cola_centro_pokemon.esta_vacia():
            print("No hay Pokemon esperando en el Centro")
            return None

        print('Enfermera Joy: "Estamos curando a tu Pokémon"')
        pokemon = self.cola_centro_pokemon.pop_front()
        pokemon.sanar()
        print(f"Procesando: [{pokemon.nombre}] -> Sanado.")

        if len(self.equipo_principal) < self.MAX_EQUIPO:
            self.equipo_principal.append(pokemon)
        else:
            self.pc.append(pokemon)

        print('Enfermera Joy: "¡Tu Pokémon está en perfecta forma!"')
        return pokemon

    def transferir_a_oak(self, pokemon):
        if not self.pc.remove_dato(pokemon):
            print(f"{pokemon.nombre} no estaba en la PC")
            return False

        if len(self.pila_transferencias) >= self.MAX_PILA_TRANSFERENCIAS:
            descartado = self.pila_transferencias.pop_back()
            print(f"(La pila de transferencias llegó al tope de {self.MAX_PILA_TRANSFERENCIAS}; "
                  f"se descartó el registro más antiguo: {descartado.nombre}.)")

        self.pila_transferencias.push_front(pokemon)
        print(f"Se transfirió a '{pokemon.nombre}' al Profesor Oak")
        return True

    def deshacer_transferencia(self):
        if self.pila_transferencias.esta_vacia():
            print("No hay transferencias para deshacer.")
            return None
        pokemon = self.pila_transferencias.pop_front()
        self.pc.append(pokemon)
        print(f"Se deshizo la transferencia de '{pokemon.nombre}' y ahora ya está de vuelta en la pc")
        return pokemon

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
            id_medio = ids_ordenados[medio]
            if id_medio == id_buscado:
                return self.pokedex[id_buscado]
            elif id_medio < id_buscado:
                izq = medio + 1
            else:
                der = medio - 1

        return None

    def _bubble_sort_por_nombre(self, lista):
        n = len(lista)
        for i in range(n):
            huevo_intercambio = False
            for j in range(0, n - i - 1):
                if lista[j].nombre.lower() > lista[j + 1].nombre.lower():
                    lista[j], lista[j + 1] = lista[j + 1], lista[j]
                    huevo_intercambio = True
            if not huevo_intercambio:
                break
        return lista

    def _insertion_sort_por_tipo(self, lista):
        for i in range(1, len(lista)):
            actual = lista[i]
            j = i - 1
            while j >= 0 and lista[j].tipo.lower() > actual.tipo.lower():
                lista[j + 1] = lista[j]
                j -= 1
            lista[j + 1] = actual
        return lista

    def _quick_sort_por_poder(self, lista):
        if len(lista) <= 1:
            return lista
        pivote = lista[len(lista) // 2].poder_combate
        mayores = [p for p in lista if p.poder_combate > pivote]
        iguales = [p for p in lista if p.poder_combate == pivote]
        menores = [p for p in lista if p.poder_combate < pivote]
        return self._quick_sort_por_poder(mayores) + iguales + self._quick_sort_por_poder(menores)

    def ordenar_pc_por_nombre(self):
        lista = self.pc.to_lista()
        lista = self._bubble_sort_por_nombre(lista)
        self.pc._reconstruir_desde_lista(lista)

    def ordenar_pc_por_tipo(self):
        lista = self.pc.to_lista()
        lista = self._insertion_sort_por_tipo(lista)
        self.pc._reconstruir_desde_lista(lista)

    def ordenar_pc_por_poder(self):
        lista = self.pc.to_lista()
        lista = self._quick_sort_por_poder(lista)
        self.pc._reconstruir_desde_lista(lista)

    def desafiar_gimnasio(self, gimnasio):
        lider = gimnasio["lider"]
        medalla = gimnasio["medalla"]
        print(f"{self.nombre} desafía al Líder {lider}")

        gano = random.choice([True, False])
        if gano:
            print(f"¡{self.nombre} derrotó a {lider}!")
            self.agregar_medalla(medalla)
        else:
            print(f"{self.nombre} perdió contra {lider}. ¡Seguí entrenando!")

        return gano