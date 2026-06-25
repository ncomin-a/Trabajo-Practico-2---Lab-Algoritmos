import json
from typing import Dict, Set

import entrenador
def pausar():
    input("\nPresione Enter para continuar...")

def ver_pokedex():
    for id, pokemon in entrenador.pokedex.items():
        print(f"ID: {id}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, Poder de Combate: {pokemon.poder_combate}")

def ver_equipo():
    for pokemon in entrenador.equipo:
        print(f"Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, Poder de Combate: {pokemon.poder_combate}")

def ver_pc():
    if entrenador.pc.esta_vacia():
        print("La PC está vacía.")
    else:
        for i, pokemon in enumerate(entrenador.pc, start=1):
            print(f"{i}. {pokemon}")
    print(f"\nTotal en PC: {len(entrenador.pc)}")
    
    
def capturar_pokemon():
    pass

def ordenar_pc():
    pass

def buscar_pokemon():
    for pokemon in entrenador.equipo:
        print(f"Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, Poder de Combate: {pokemon.poder_combate}")

def consultar_ID():
    pass

def enviar_pokemon():
    pass

def transferir_pokemon():
    pass

def deshacer_transf():
    pass

def desafiar_gym():
    pass

def ver_medallas():
    if not entrenador.medallas:
        print("No ganaste ninguna medalla aún.")
    else:
        for medalla in entrenador.medallas:
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