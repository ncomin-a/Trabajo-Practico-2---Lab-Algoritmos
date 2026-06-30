class Pokemon:
    def __init__(self, id_pokemon: int, nombre: str, tipo: str):
        self.id = id_pokemon
        self.nombre = nombre
        self.tipo = tipo

    def __str__(self):
        return f"Pokémon(ID: {self.id}, Nombre: {self.nombre}, Tipo: {self.tipo})"
   
