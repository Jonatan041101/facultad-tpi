"""Interfaz de consola del sistema de gestión de países."""

from countries_repository import load_countries, save_countries
from countries_service import (
    add_country,
    filter_by_area_range,
    filter_by_continent,
    filter_by_population_range,
    search_countries_by_name,
    sort_countries,
    update_country,
)
from countries_stats import (
    count_by_continent,
    get_average_area,
    get_average_population,
    get_country_with_max_population,
    get_country_with_min_population,
)


def display_countries(countries):
    """Presenta una colección de países como tabla."""
    if not countries:
        print("No se encontraron resultados.")
        return

    print(f"{'Nombre':<20} | {'Continente':<18} | {'Población':>12} | {'Superficie km²':>15}")
    print("-" * 75)
    for country in countries:
        print(
            f"{country['name']:<20} | {country['continent']:<18} | "
            f"{country['population']:>12,} | {country['area']:>15,.2f}"
        )


def _add_country(countries):
    print("\n--- AGREGAR PAÍS ---")
    country = add_country(countries, {
        "name": input("Nombre: "),
        "continent": input("Continente: "),
        "population": input("Población (entero positivo): "),
        "area": input("Superficie en km² (número positivo): "),
    })
    save_countries(countries)
    print(f"{country['name']} fue agregado y guardado.")


def _update_country(countries):
    print("\n--- ACTUALIZAR PAÍS ---")
    country = update_country(
        countries,
        input("Nombre del país: "),
        input("Nueva población: "),
        input("Nueva superficie en km²: "),
    )
    if country is None:
        print("País no encontrado.")
        return
    save_countries(countries)
    print(f"{country['name']} fue actualizado y guardado.")


def _search(countries):
    print("\n--- BUSCAR PAÍS ---")
    display_countries(search_countries_by_name(countries, input("Nombre o parte: ")))


def _filter(countries):
    print("\n--- FILTRAR PAÍSES ---")
    print("1. Continente\n2. Rango de población\n3. Rango de superficie")
    option = input("Opción: ").strip()
    if option == "1":
        result = filter_by_continent(countries, input("Continente: "))
    elif option == "2":
        result = filter_by_population_range(
            countries, input("Población mínima: "), input("Población máxima: ")
        )
    elif option == "3":
        result = filter_by_area_range(
            countries, input("Superficie mínima: "), input("Superficie máxima: ")
        )
    else:
        raise ValueError("La opción de filtro no es válida.")
    display_countries(result)


def _sort(countries):
    print("\n--- ORDENAR PAÍSES ---")
    print("1. Nombre\n2. Población\n3. Superficie")
    criteria = {"1": "name", "2": "population", "3": "area"}
    criterion = criteria.get(input("Criterio: ").strip())
    if criterion is None:
        raise ValueError("El criterio de ordenamiento no es válido.")
    direction = input("1. Ascendente | 2. Descendente: ").strip()
    if direction not in ("1", "2"):
        raise ValueError("El sentido de ordenamiento no es válido.")
    display_countries(sort_countries(countries, criterion, direction == "2"))


def _show_statistics(countries):
    maximum = get_country_with_max_population(countries)
    minimum = get_country_with_min_population(countries)
    print("\n--- ESTADÍSTICAS ---")
    print(f"Mayor población: {maximum['name']} ({maximum['population']:,})")
    print(f"Menor población: {minimum['name']} ({minimum['population']:,})")
    print(f"Población promedio: {get_average_population(countries):,.2f}")
    print(f"Superficie promedio: {get_average_area(countries):,.2f} km²")
    print("Países por continente:")
    for continent, amount in sorted(count_by_continent(countries).items()):
        print(f"  - {continent}: {amount}")


def _print_menu():
    print("\n========================================")
    print("     SISTEMA DE GESTIÓN DE PAÍSES")
    print("========================================")
    print("1. Agregar país")
    print("2. Actualizar población y superficie")
    print("3. Buscar por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("7. Salir")


def run_menu():
    """Carga los datos y mantiene activo el menú hasta que el usuario sale."""
    try:
        countries = load_countries()
    except (OSError, ValueError) as error:
        print(f"No fue posible iniciar el sistema: {error}")
        return

    actions = {
        "1": _add_country,
        "2": _update_country,
        "3": _search,
        "4": _filter,
        "5": _sort,
        "6": _show_statistics,
    }

    while True:
        _print_menu()
        option = input("Seleccione una opción (1-7): ").strip()
        if option == "7":
            print("Datos guardados. ¡Hasta luego!")
            break
        action = actions.get(option)
        if action is None:
            print("Opción inválida. Intente nuevamente.")
            continue
        try:
            action(countries)
        except (OSError, ValueError) as error:
            print(f"Error: {error}")
