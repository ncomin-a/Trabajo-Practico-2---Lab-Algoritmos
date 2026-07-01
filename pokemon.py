class Pokemon:
    def __init__(self, id_pokemon: int, nombre: str, tipo: str, poder_combate: int):
        self.id = id_pokemon
        self.nombre = nombre
        self.tipo = tipo
        self.poder_combate = poder_combate

    def sanar(self):
        self.hp = self.hp_max

    def __str__(self):
        return f"Pokemon(ID: {self.id}, Nombre: {self.nombre}, Tipo: {self.tipo}, Poder de Combate: {self.poder_combate}))"
    
