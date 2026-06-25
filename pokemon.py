class Pokemon:
    def __init__(self, id_pokemon: int, nombre: str, tipo: str, poder_combate: int, hp: int, nivel: int):
        self.id = id_pokemon
        self.nombre = nombre
        self.tipo = tipo
        self.poder_combate = poder_combate
        self.hp = hp
        self.nivel = nivel

    def sanar(self):
        self.hp = max(self.hp, 1)

    def __str__(self):
        return f"Pokémon(ID: {self.id}, Nombre: {self.nombre}, Tipo: {self.tipo}, Poder de Combate: {self.poder_combate}, HP: {self.hp}, Nivel: {self.nivel})"
   
