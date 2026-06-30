import json
from typing import Dict, Set
import random

from entrenador import Entrenador, GIMNASIOS

jugador = Entrenador("Ash")

def pausar():
    input("\nPresione Enter para continuar...")

def ver_pokedex():
    if not jugador.pokedex:
        print("La Pokédex está vacía.")
        return
    for id_pokemon, pokemon in jugador.pokedex.items():
        print(f"ID: {id_pokemon}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, ")
        
def ver_equipo():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return
    for pokemon in jugador.equipo_principal:
        print(f"ID: {pokemon.id}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, ")
        
def ver_pc():
    if jugador.pc.esta_vacia():
        print("La PC está vacía.")
    else:
        for i, pokemon in enumerate(jugador.pc, start=1):
            print(f"{i}. {pokemon}")
    print(f"\nTotal en PC: {len(jugador.pc)}")


def capturar_pokemon():
    nuevo = jugador.generar_pokemon_aleatorio()
    print(f"¡Apareció {nuevo.nombre} ({nuevo.tipo})!")
    jugador.capturar_pokemon(nuevo)

def ordenar_pc():
    if not jugador.pc:
        print("La PC está vacía, no hay nada para ordenar.")
        return

    print("¿Por qué criterio querés ordenar la PC?")
    print(" 1. Poder de combate")
    print(" 2. Nombre")
    print(" 3. Nivel")
    criterio = input("Opción: ").strip()
    if criterio == "1":
        jugador.pc.ordenar_por_poder()
    elif criterio == "2":
        jugador.pc.ordenar_por_nombre()
    elif criterio == "3":
        jugador.pc.ordenar_por_nivel()
    else:
        print("Opción inválida.")

def buscar_pokemon():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return
    
    nombre_buscar = input("Ingrese el nombre del Pokémon que desea buscar: ").strip().lower()
    encontrados = [pokemon for pokemon in jugador.equipo_principal if pokemon.nombre.lower() == nombre_buscar]
    if encontrados:
        print("Pokémones encontrados:")
        for pokemon in encontrados:
            print(f"ID: {pokemon.id}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}")
    else:
        print("No se encontró ningún Pokémon con ese nombre.")

def consultar_ID():
    id_pokemon = input("Ingrese el ID del Pokémon que desea consultar: ")
    if id_pokemon.isdigit():
        id_pokemon = int(id_pokemon)
        if id_pokemon in jugador.pokedex:
            pokemon = jugador.pokedex[id_pokemon]
            print(f"ID: {pokemon.id}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}")
        else:
            print(f"No se encontró un Pokémon con ID {id_pokemon}.")
    

def enviar_pokemon():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return

    print("Pokémones en el equipo principal:")
    for i, pokemon in enumerate(jugador.equipo_principal, start=1):
        print(f"{i}. {pokemon.nombre} (ID: {pokemon.id}, Tipo: {pokemon.tipo})")

    try:
        indice = int(input("Ingrese el número del Pokémon que desea enviar al Centro Pokémon: ")) - 1
        if 0 <= indice < len(jugador.equipo_principal):
            pokemon_a_enviar = jugador.equipo_principal[indice]
            jugador.enviar_pokemon_centro(pokemon_a_enviar)
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número válido.")

def transferir_pokemon():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return

    print("Pokémones en el equipo principal:")
    for i, pokemon in enumerate(jugador.equipo_principal, start=1):
        print(f"{i}. {pokemon.nombre} (ID: {pokemon.id}, Tipo: {pokemon.tipo})")

    try:
        indice = int(input("Ingrese el número del Pokémon que desea transferir al Profesor Oak: ")) - 1
        if 0 <= indice < len(jugador.equipo_principal):
            pokemon_a_transferir = jugador.equipo_principal[indice]
            jugador.transferir_pokemon(pokemon_a_transferir, jugador)
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número válido.")

def deshacer_transf():
    pass

def desafiar_gym():
    print("Gimnasios disponibles:")
    for gimnasio in GIMNASIOS:
        print(f" {gimnasio['numero']}. Líder {gimnasio['lider']} - {gimnasio['medalla']}")

    try:
        numero = int(input("Ingrese el número del gimnasio a desafiar: "))
    except ValueError:
        print("Número inválido.")
        return
    
    gimnasio = next((g for g in GIMNASIOS if g['numero'] == numero), None)
    if gimnasio is None:
        print("Gimnasio no encontrado.")
        return
    resultado = random.choice([True, False])
    if resultado:
        print(f"¡Felicidades! Has derrotado al líder {gimnasio['lider']} y obtenido la medalla {gimnasio['medalla']}!")
        jugador.medallas.append({"nombre": gimnasio['medalla'], "gimnasio": gimnasio['lider']})
    else:
        print(f"Has sido derrotado por el líder {gimnasio['lider']}. ¡Sigue intentando!")
    

def ver_medallas():
    if not jugador.medallas:
        print("No ganaste ninguna medalla aún.")
    else:
        for medalla in jugador.medallas:
            print(f"Medalla: {medalla['nombre']}, Gimnasio: {medalla['gimnasio']}")

def salir_sistema():
    print("Saliendo del sistema. ¡Hasta luego!")
    exit(0)

def mostrar_menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print(" 1. Ver Pokédex")
    print(" 2. Ver Equipo Principal")
    print(" 3. Ver PC")
    print(" 4. Capturar nuevo Pokémon")
    print(" 5. Ordenar PC")
    print(" 6. Buscar Pokémon en Equipo")
    print(" 7. Consultar Pokémon en Pokédex por ID")
    print(" 8. Enviar Pokémon al Centro Pokémon")
    print(" 9. Transferir Pokémon al Profesor Oak")
    print("10. Deshacer última transferencia")
    print("11. Desafiar Líder de Gimnasio")
    print("12. Ver Medallas")
    print("13. Salir del sistema")

def main():
    mostrar_menu()
    
    opcion = input("Seleccione una opción (1-13): ")

    match opcion:
        case "1":
            ver_pokedex()
        case "2":   
            ver_equipo()
        case "3":
            ver_pc()
        case "4":
            capturar_pokemon()
        case "5":
            ordenar_pc()
        case "6":
            buscar_pokemon()
        case "7":
            consultar_ID()
        case "8":
            enviar_pokemon()
        case "9":
            transferir_pokemon()
        case "10":
            deshacer_transf()
        case "11":
            desafiar_gym()
        case "12":
            ver_medallas()
        case "13":
            salir_sistema()
        case _:
            print("Opción inválida. Por favor, seleccione una opción del 1 al 13.")

if __name__ == "__main__":
    main()