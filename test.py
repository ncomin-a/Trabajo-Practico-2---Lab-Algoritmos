"""
Módulo 5: Menú Interactivo
----------------------------
Punto de entrada del sistema "Pokémon Huergo". Ejecutar con:

    python main.py
"""

import os
import time

from entrenador import Entrenador, GIMNASIOS
from algoritmos import (
    bubble_sort_por_nombre,
    insertion_sort_por_tipo,
    quick_sort_por_poder_combate,
    busqueda_lineal_por_nombre,
    busqueda_binaria_por_id,
)

RUTA_POKEDEX = os.path.join(os.path.dirname(__file__), "data", "pokedex.json")
RUTA_MEDALLAS = os.path.join(os.path.dirname(__file__), "data", "medallas.json")


# ---------------------------------------------------------------------------
# UTILIDADES DE INTERFAZ
# ---------------------------------------------------------------------------

def pausar():
    input("\nPresione ENTER para continuar...")


def pedir_entero(mensaje):
    """Pide un entero por consola, validando la entrada y repitiendo si
    es inválida."""
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            print("Por favor ingrese un número entero válido.")


def imprimir_encabezado(titulo):
    print("\n" + "=" * 50)
    print(titulo.center(50))
    print("=" * 50)


# ---------------------------------------------------------------------------
# INICIALIZACIÓN
# ---------------------------------------------------------------------------

def inicializar_sistema():
    imprimir_encabezado("SISTEMA DE GESTIÓN: POKÉMON HUERGO")
    print("Inicializando motor de base de datos... OK.")

    entrenador = Entrenador()

    cantidad_pokemon = entrenador.cargar_pokedex_desde_json(RUTA_POKEDEX)
    print(f"Cargando Pokédex Nacional ({cantidad_pokemon} registros)... OK.")

    cantidad_medallas = entrenador.cargar_medallas_desde_json(RUTA_MEDALLAS)
    print(f"Validando registros de medallas ({cantidad_medallas} precargadas)... OK.")

    time.sleep(0.3)
    return entrenador


# ---------------------------------------------------------------------------
# OPCIONES DEL MENÚ
# ---------------------------------------------------------------------------

def ver_pokedex(entrenador):
    imprimir_encabezado("POKÉDEX NACIONAL")
    for id_pokemon in sorted(entrenador.pokedex.keys()):
        print(entrenador.pokedex[id_pokemon])
    print(f"\nTotal de registros: {len(entrenador.pokedex)}")
    pausar()


def ver_equipo_principal(entrenador):
    imprimir_encabezado("EQUIPO PRINCIPAL")
    if not entrenador.equipo_principal:
        print("El equipo está vacío.")
    else:
        for i, pokemon in enumerate(entrenador.equipo_principal, start=1):
            print(f"{i}. {pokemon}")
    print(f"\nOcupación: {len(entrenador.equipo_principal)}/{entrenador.MAX_EQUIPO}")
    pausar()


def ver_pc(entrenador):
    imprimir_encabezado("ALMACENAMIENTO (PC)")
    if entrenador.pc.esta_vacia():
        print("La PC está vacía.")
    else:
        for i, pokemon in enumerate(entrenador.pc, start=1):
            print(f"{i}. {pokemon}")
    print(f"\nTotal en PC: {len(entrenador.pc)}")
    pausar()


def capturar_pokemon(entrenador):
    imprimir_encabezado("SISTEMA DE CAPTURA")
    nuevo_pokemon = entrenador.generar_pokemon_salvaje()
    print(f"Ha aparecido un {nuevo_pokemon.nombre.upper()} salvaje (PC: {nuevo_pokemon.poder_combate}).")
    print("¡Captura exitosa!")
    print("Analizando espacios...")

    destino = entrenador.capturar_pokemon(nuevo_pokemon)

    if destino == "EQUIPO":
        print(f"Hay lugar en el Equipo Principal ({len(entrenador.equipo_principal)}/{entrenador.MAX_EQUIPO}).")
        print(f"'{nuevo_pokemon.nombre}' se unió al Equipo Principal.")
    else:
        print(f"El Equipo Principal está lleno ({entrenador.MAX_EQUIPO}/{entrenador.MAX_EQUIPO}).")
        print("Derivando a Almacenamiento de PC... Registro añadido exitosamente.")
    pausar()


def submenu_ordenar_pc(entrenador):
    imprimir_encabezado("ORDENAR PC")
    if entrenador.pc.esta_vacia():
        print("La PC está vacía, no hay nada para ordenar.")
        pausar()
        return

    print("1. Alfabético (Bubble Sort, A-Z)")
    print("2. Por Tipo (Insertion Sort)")
    print("3. Por Poder de Combate (Quick Sort, mayor a menor)")
    print("4. Volver")
    opcion = input("Seleccione una opción: ").strip()

    lista_temporal = entrenador.pc.a_lista_python()

    if opcion == "1":
        bubble_sort_por_nombre(lista_temporal)
        print("\nPC ordenada alfabéticamente:")
    elif opcion == "2":
        insertion_sort_por_tipo(lista_temporal)
        print("\nPC ordenada por tipo:")
    elif opcion == "3":
        quick_sort_por_poder_combate(lista_temporal)
        print("\nPC ordenada por poder de combate (mayor a menor):")
    elif opcion == "4":
        return
    else:
        print("Opción inválida.")
        pausar()
        return

    entrenador.pc.reconstruir_desde_lista(lista_temporal)
    for i, pokemon in enumerate(entrenador.pc, start=1):
        print(f"{i}. {pokemon}")
    pausar()


def buscar_en_equipo(entrenador):
    imprimir_encabezado("BÚSQUEDA EN EQUIPO (Lineal)")
    if not entrenador.equipo_principal:
        print("El equipo está vacío.")
        pausar()
        return

    nombre = input("Ingrese el nombre del Pokémon a buscar: ").strip()
    encontrado = busqueda_lineal_por_nombre(entrenador.equipo_principal, nombre)

    if encontrado:
        print(f"\n¡Encontrado! {encontrado} está en tu Equipo Principal.")
    else:
        print(f"\n'{nombre}' no se encuentra en tu Equipo Principal.")
    pausar()


def consultar_pokedex_por_id(entrenador):
    imprimir_encabezado("CONSULTA EN POKÉDEX (Búsqueda Binaria)")
    id_buscado = pedir_entero("Ingrese el ID a buscar: ")
    ids_ordenados = entrenador.obtener_ids_ordenados()
    resultado = busqueda_binaria_por_id(ids_ordenados, entrenador.pokedex, id_buscado)

    if resultado:
        print(f"\n¡Registro encontrado! {resultado}")
    else:
        print(f"\nNo existe ningún Pokémon con ID {id_buscado} en la Pokédex Nacional.")
    pausar()


def enviar_al_centro_pokemon(entrenador):
    imprimir_encabezado("CENTRO POKÉMON - COLA DE SANACIÓN")
    if not entrenador.equipo_principal:
        print("No tenés Pokémon en el equipo para sanar.")
        pausar()
        return

    print("Ingresando equipo a la cola...")
    print('Enfermera Joy: "Estamos curando a tus Pokémon..."')
    time.sleep(0.3)

    procesados = entrenador.sanar_equipo()
    for nombre in procesados:
        print(f"Procesando: [{nombre}] -> Sanado.")
        time.sleep(0.15)

    print('Enfermera Joy: "¡Tus Pokémon están en perfecta forma!"')
    pausar()


def transferir_al_oak(entrenador):
    imprimir_encabezado("SISTEMA DE TRANSFERENCIAS")
    if entrenador.pc.esta_vacia():
        print("No hay Pokémon en la PC para transferir.")
        pausar()
        return

    print("Pokémon disponibles en la PC:")
    for i, pokemon in enumerate(entrenador.pc, start=1):
        print(f"{i}. {pokemon}")

    nombre = input("\nIngrese el nombre del Pokémon a transferir: ").strip()
    transferido = entrenador.transferir_al_profesor_oak(nombre)

    if transferido:
        print(f"\nHa transferido a '{transferido.nombre}' al Profesor Oak.")
        print(f"(Pila de transferencias: {len(entrenador.pila_transferencias)}/{entrenador.MAX_PILA_TRANSFERENCIAS})")
    else:
        print(f"\nNo se encontró a '{nombre}' en la PC.")
    pausar()


def deshacer_transferencia(entrenador):
    imprimir_encabezado("DESHACER ÚLTIMA TRANSFERENCIA")
    if entrenador.pila_transferencias.esta_vacia():
        print("No hay transferencias para deshacer.")
        pausar()
        return

    print("> Operación: Deshacer transferencia")
    recuperado = entrenador.deshacer_ultima_transferencia()
    print(f"Recuperando último registro... '{recuperado.nombre}' ha vuelto a la PC.")
    pausar()


def desafiar_lider_gimnasio(entrenador):
    imprimir_encabezado("DESAFÍO A LÍDER DE GIMNASIO")
    print("Gimnasios disponibles:")
    for g in GIMNASIOS:
        ya_obtenida = "✓" if g["medalla"] in entrenador.medallas else " "
        print(f"{g['numero']}. {g['lider']:<10} -> {g['medalla']} [{ya_obtenida}]")

    numero = pedir_entero("\nElegí el número de gimnasio a desafiar: ")
    resultado = entrenador.desafiar_gimnasio(numero)

    if not resultado["valido"]:
        print("Ese gimnasio no existe.")
        pausar()
        return

    print(f"\n¡Comienza la batalla contra {resultado['lider']}!")
    time.sleep(0.4)

    if resultado["gano"]:
        print(f"¡Ganaste! {resultado['lider']} te entrega la {resultado['medalla']}.")
        if resultado["medalla_nueva"]:
            print(f"'{resultado['medalla']}' agregada al registro de medallas.")
        else:
            print(f"Ya tenías la '{resultado['medalla']}'; el Hash Set evitó el duplicado.")
    else:
        print(f"Perdiste contra {resultado['lider']}. ¡Intentalo de nuevo!")

    print(f"\nMedallas obtenidas: {len(entrenador.medallas)}/{len(GIMNASIOS)}")
    pausar()


def ver_medallas(entrenador):
    imprimir_encabezado("REGISTRO DE MEDALLAS")
    if not entrenador.medallas:
        print("Todavía no tenés medallas.")
    else:
        for medalla in sorted(entrenador.medallas):
            print(f"- {medalla}")
    print(f"\nTotal: {len(entrenador.medallas)}/{len(GIMNASIOS)}")
    pausar()


# ---------------------------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------------------------

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
    entrenador = inicializar_sistema()

    opciones = {
        "1": lambda: ver_pokedex(entrenador),
        "2": lambda: ver_equipo_principal(entrenador),
        "3": lambda: ver_pc(entrenador),
        "4": lambda: capturar_pokemon(entrenador),
        "5": lambda: submenu_ordenar_pc(entrenador),
        "6": lambda: buscar_en_equipo(entrenador),
        "7": lambda: consultar_pokedex_por_id(entrenador),
        "8": lambda: enviar_al_centro_pokemon(entrenador),
        "9": lambda: transferir_al_oak(entrenador),
        "10": lambda: deshacer_transferencia(entrenador),
        "11": lambda: desafiar_lider_gimnasio(entrenador),
        "12": lambda: ver_medallas(entrenador),
    }

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "13":
            print("\n¡Gracias por jugar Pokémon Huergo! Hasta la próxima.")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()