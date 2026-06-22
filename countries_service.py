"""Reglas de negocio y operaciones sobre países."""

from countries_validations import (
    validate_country_data,
    validate_positive_number,
    validate_range,
    validate_required_text,
)


def add_country(countries, country_data):
    """Valida y agrega un país si su nombre no está registrado."""
    country = validate_country_data(country_data)
    normalized_name = country["name"].casefold()

    if any(item["name"].casefold() == normalized_name for item in countries):
        raise ValueError("El país ya se encuentra registrado.")

    countries.append(country)
    return country


def update_country(countries, name, population, area):
    """Actualiza población y superficie; devuelve None si no existe."""
    searched_name = validate_required_text(name, "El nombre").casefold()
    validated_population = validate_positive_number(
        population, "La población", int
    )
    validated_area = validate_positive_number(area, "La superficie", float)

    for country in countries:
        if country["name"].casefold() == searched_name:
            country["population"] = validated_population
            country["area"] = validated_area
            return country
    return None


def search_countries_by_name(countries, query):
    """Busca coincidencias parciales sin distinguir mayúsculas."""
    normalized_query = validate_required_text(query, "La búsqueda").casefold()
    return [
        country for country in countries
        if normalized_query in country["name"].casefold()
    ]


def filter_by_continent(countries, continent):
    """Filtra por coincidencia exacta de continente."""
    normalized = validate_required_text(continent, "El continente").casefold()
    return [
        country for country in countries
        if country["continent"].casefold() == normalized
    ]


def filter_by_population_range(countries, minimum, maximum):
    """Filtra por un rango inclusivo de población."""
    minimum, maximum = validate_range(minimum, maximum, "La población", int)
    return [
        country for country in countries
        if minimum <= country["population"] <= maximum
    ]


def filter_by_area_range(countries, minimum, maximum):
    """Filtra por un rango inclusivo de superficie."""
    minimum, maximum = validate_range(minimum, maximum, "La superficie", float)
    return [
        country for country in countries
        if minimum <= country["area"] <= maximum
    ]


def sort_countries(countries, criterion, descending=False):
    """Devuelve una nueva lista ordenada sin modificar la original."""
    keys = {
        "name": lambda country: country["name"].casefold(),
        "population": lambda country: country["population"],
        "area": lambda country: country["area"],
    }
    if criterion not in keys:
        raise ValueError("El criterio de ordenamiento no es válido.")
    return sorted(countries, key=keys[criterion], reverse=descending)
