"""Cálculo de indicadores estadísticos de países."""


def _require_countries(countries):
    if not countries:
        raise ValueError("No hay países para calcular estadísticas.")


def get_country_with_max_population(countries):
    _require_countries(countries)
    return max(countries, key=lambda country: country["population"])


def get_country_with_min_population(countries):
    _require_countries(countries)
    return min(countries, key=lambda country: country["population"])


def get_average_population(countries):
    _require_countries(countries)
    return sum(country["population"] for country in countries) / len(countries)


def get_average_area(countries):
    _require_countries(countries)
    return sum(country["area"] for country in countries) / len(countries)


def count_by_continent(countries):
    """Devuelve un diccionario de frecuencias por continente."""
    counts = {}
    for country in countries:
        continent = country["continent"]
        counts[continent] = counts.get(continent, 0) + 1
    return counts
