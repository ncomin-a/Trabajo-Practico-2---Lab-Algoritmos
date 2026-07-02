from entrenador import Entrenador, GIMNASIOS

jugador = Entrenador("Ash")
profesor_oak = Entrenador("Profesor Oak")


def pausar():
    input("\nPresione Enter para continuar...")


def inicializar():
    cargados = jugador.cargar_pokedex_desde_json("pokemons.json")
    print(f"Se cargaron {cargados} Pokemon en la Pokedex de {jugador.nombre}")
    cant_medallas = jugador.cargar_medallas_desde_json("medallas.json")
    print(f"Se cargaron {cant_medallas} medallas disponibles")


def ver_pokedex():
    if len(jugador.pokedex) == 0:
        print("La Pokedex esta vacia.")
        return
    for id_pokemon, pokemon in jugador.pokedex.items():
        print(f"ID: {id_pokemon}, Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, Poder de Combate: {pokemon.poder_combate}")


def ver_equipo():
    if len(jugador.equipo_principal) == 0:
        print("El equipo principal está vacio.")
        return
    for pokemon in jugador.equipo_principal:
        print(f"Nombre: {pokemon.nombre}, Tipo: {pokemon.tipo}, Poder de Combate: {pokemon.poder_combate}, HP: {pokemon.hp}/{pokemon.hp_max}")


def ver_pc():
    if len(jugador.pc) == 0:
        print("La PC esta vacía.")
    else:
        i = 1
        for pokemon in jugador.pc:
            print(f"{i}. {pokemon}")
            i += 1
    print(f"\nTotal en PC: {len(jugador.pc)}")


def capturar_pokemon():
    jugador.capturar_pokemon()


def ordenar_pc():
    if len(jugador.pc) == 0:
        print("La PC esta vacía")
        return

    print("Por qué criterio querés ordenar la PC?")
    print(" 1. Nombre")
    print(" 2. Tipo")
    print(" 3. Poder de combate")
    criterio = input("Opcion: ")

    if criterio == "1":
        jugador.ordenar_pc_por_nombre()
        print("PC ordenada por nombre (alfabético)")
    elif criterio == "2":
        jugador.ordenar_pc_por_tipo()
        print("PC ordenada por tipo (alfabético)")
    elif criterio == "3":
        jugador.ordenar_pc_por_poder()
        print("PC ordenada por poder de combate (de mayor a menor)")
    else:
        print("Opción inválida. No se ordenó la PC")
        return

    ver_pc()


def buscar_pokemon():
    if len(jugador.equipo_principal) == 0:
        print("El equipo principal esta vacío")
        return

    nombre_buscado = input("Nombre del Pokemon a buscar: ")
    pokemon = jugador.busqueda_lineal_equipo(nombre_buscado)

    if pokemon is None:
        print(f"No se encontró a '{nombre_buscado}' en el equipo principal")
    else:
        print(pokemon)


def consultar_ID():
    try:
        id_pokemon = int(input("Ingrese el ID del Pokemon a consultar: "))
    except ValueError:
        print("ID invalido, tiene que ser un número.")
        return

    pokemon = jugador.busqueda_binaria_pokedex(id_pokemon)
    if pokemon is None:
        print(f"No hay ningun Pokemon con ID {id_pokemon} en la Pokedex")
    else:
        print(pokemon)


def enviar_pokemon():
    if len(jugador.equipo_principal) == 0:
        print("El equipo principal esta vacío.")
        return

    nombre_buscado = input("Nombre del Pokemon a enviar al Centro Pokemon: ").lower()

    pokemon = None
    for p in jugador.equipo_principal:
        if p.nombre.lower() == nombre_buscado:
            pokemon = p
            break

    if pokemon is None:
        print(f"'{nombre_buscado}' no está en el equipo principal")
        return

    jugador.enviar_pokemon_centro(pokemon)
    jugador.atender_siguiente_en_centro()


def transferir_pokemon():
    if len(jugador.equipo_principal) == 0 and len(jugador.pc) == 0:
        print("No tenés Pokemon en la PC para transferir.")
        return

    nombre_buscado = input("Nombre del Pokemon a transferir al Profesor Oak (tiene que estar en la PC): ").lower()

    pokemon = None
    for p in jugador.pc:
        if p.nombre.lower() == nombre_buscado:
            pokemon = p
            break

    if pokemon is None:
        print(f"'{nombre_buscado}' no está en la PC")
        return

    jugador.transferir_a_oak(pokemon)


def deshacer_transf():
    jugador.deshacer_transferencia()


def desafiar_gym():
    print("Gimnasios disponibles:")
    for gimnasio in GIMNASIOS:
        print(f" {gimnasio['numero']}. Lider {gimnasio['lider']} - {gimnasio['medalla']}")

    try:
        numero = int(input("Ingrese el número del gimnasio a desafiar: "))
    except ValueError:
        print("Número inválido.")
        return

    gimnasio_elegido = None
    for g in GIMNASIOS:
        if g["numero"] == numero:
            gimnasio_elegido = g
            break

    if gimnasio_elegido is None:
        print(f"El gimnasio {numero} no existe")
        return

    jugador.desafiar_gimnasio(gimnasio_elegido)


def ver_medallas():
    if len(jugador.medallas) == 0:
        print("No ganaste ninguna medalla todavía")
    else:
        for medalla in jugador.medallas:
            print(f"Medalla: {medalla}")


def salir_sistema():
    print("Saliendo... hasta luego!")
    exit(0)


def mostrar_menu():
    print("\n--- MENU PRINCIPAL ---")
    print(" 1. Ver Pokedex")
    print(" 2. Ver Equipo Principal")
    print(" 3. Ver PC")
    print(" 4. Capturar nuevo Pokemon")
    print(" 5. Ordenar PC")
    print(" 6. Buscar Pokemon en Equipo")
    print(" 7. Consultar Pokemon en Pokedex por ID")
    print(" 8. Enviar Pokemon al Centro Pokemon")
    print(" 9. Transferir Pokemon al Profesor Oak")
    print("10. Deshacer ultima transferencia")
    print("11. Desafiar Lider de Gimnasio")
    print("12. Ver Medallas")
    print("13. Salir del sistema")


def main():
    inicializar()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion (1-13): ")

        if opcion == "1":
            ver_pokedex()
        elif opcion == "2":
            ver_equipo()
        elif opcion == "3":
            ver_pc()
        elif opcion == "4":
            capturar_pokemon()
        elif opcion == "5":
            ordenar_pc()
        elif opcion == "6":
            buscar_pokemon()
        elif opcion == "7":
            consultar_ID()
        elif opcion == "8":
            enviar_pokemon()
        elif opcion == "9":
            transferir_pokemon()
        elif opcion == "10":
            deshacer_transf()
        elif opcion == "11":
            desafiar_gym()
        elif opcion == "12":
            ver_medallas()
        elif opcion == "13":
            salir_sistema()
        else:
            print("Opción inválida, ingresa un número del 1 al 13.")

        pausar()


if __name__ == "__main__":
    main()