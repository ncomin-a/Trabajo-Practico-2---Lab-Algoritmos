from entrenador import Entrenador, GIMNASIOS


# Estado global del programa: el entrenador del jugador y el Profesor Oak,
# que existe únicamente para recibir transferencias (y poder devolverlas).
jugador = Entrenador("Ash")
profesor_oak = Entrenador("Profesor Oak")


def pausar():
    input("\nPresione Enter para continuar...")


def inicializar():
    cargados = jugador.cargar_pokedex_desde_json("pokemons.json")
    print(f"Se cargaron {cargados} Pokémon en la Pokédex de {jugador.nombre}.")
    cant_medallas = jugador.cargar_medallas_desde_json("medallas.json")
    print(f"Se cargaron {cant_medallas} medallas disponibles.")


def ver_pokedex():
    if not jugador.pokedex:
        print("La Pokédex está vacía.")
        return
    for id_pokemon, pokemon in jugador.pokedex.items():
        print(f"ID: {id_pokemon}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, "
              f"Poder de Combate: {pokemon.poder_combate}")


def ver_equipo():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return
    for pokemon in jugador.equipo_principal:
        print(f"Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, "
              f"Poder de Combate: {pokemon.poder_combate}, HP: {pokemon.hp}")


def ver_pc():
    if not jugador.pc:
        print("La PC está vacía.")
    else:
        for i, pokemon in enumerate(jugador.pc, start=1):
            print(f"{i}. {pokemon}")
    print(f"\nTotal en PC: {len(jugador.pc)}")


def capturar_pokemon():
    nuevo = jugador.generar_pokemon_aleatorio()
    print(f"¡Apareció {nuevo.nombre} ({nuevo.tipo}, Poder de Combate {nuevo.poder_combate})!")
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
        jugador.pc.sort(key=lambda p: p.poder_combate, reverse=True)
        print("PC ordenada por poder de combate (de mayor a menor).")
    elif criterio == "2":
        jugador.pc.sort(key=lambda p: p.nombre)
        print("PC ordenada por nombre (alfabético).")
    elif criterio == "3":
        jugador.pc.sort(key=lambda p: p.nivel, reverse=True)
        print("PC ordenada por nivel (de mayor a menor).")
    else:
        print("Opción inválida. No se ordenó la PC.")
        return

    ver_pc()


def buscar_pokemon():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return

    nombre_buscado = input("Nombre del Pokémon a buscar: ").strip().lower()
    encontrados = [p for p in jugador.equipo_principal if p.nombre.lower() == nombre_buscado]

    if not encontrados:
        print(f"No se encontró a '{nombre_buscado}' en el equipo principal.")
        return

    for pokemon in encontrados:
        print(pokemon)


def consultar_ID():
    try:
        id_pokemon = int(input("Ingrese el ID del Pokémon a consultar: "))
    except ValueError:
        print("ID inválido, debe ser un número.")
        return

    pokemon = jugador.consultar_pokemon_por_id(id_pokemon)
    if pokemon is None:
        print(f"No hay ningún Pokémon con ID {id_pokemon} en la Pokédex.")
    else:
        print(pokemon)


def enviar_pokemon():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío.")
        return

    nombre_buscado = input("Nombre del Pokémon a enviar al Centro Pokémon: ").strip().lower()
    pokemon = next((p for p in jugador.equipo_principal if p.nombre.lower() == nombre_buscado), None)

    if pokemon is None:
        print(f"'{nombre_buscado}' no está en el equipo principal.")
        return

    jugador.enviar_pokemon_centro(pokemon)
    jugador.atender_siguiente_en_centro()


def transferir_pokemon():
    if not jugador.equipo_principal:
        print("El equipo principal está vacío, no hay nada para transferir.")
        return

    nombre_buscado = input("Nombre del Pokémon a transferir al Profesor Oak: ").strip().lower()
    pokemon = next((p for p in jugador.equipo_principal if p.nombre.lower() == nombre_buscado), None)

    if pokemon is None:
        print(f"'{nombre_buscado}' no está en el equipo principal.")
        return

    jugador.transferir_pokemon(pokemon, profesor_oak)


def deshacer_transf():
    jugador.deshacer_transferencia()


def desafiar_gym():
    print("Gimnasios disponibles:")
    for gimnasio in GIMNASIOS:
        print(f" {gimnasio['numero']}. Líder {gimnasio['lider']} - {gimnasio['medalla']}")

    try:
        numero = int(input("Ingrese el número del gimnasio a desafiar: "))
    except ValueError:
        print("Número inválido.")
        return

    gimnasio = next((g for g in GIMNASIOS if g["numero"] == numero), None)
    if gimnasio is None:
        print(f"El gimnasio {numero} no existe.")
        return

    jugador.desafiar_gimnasio(gimnasio)
    jugador.agregar_medalla({"nombre": gimnasio["medalla"], "gimnasio": f"Gimnasio {gimnasio['numero']}"})


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
    inicializar()

    while True:
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

        pausar()


if __name__ == "__main__":
    main()