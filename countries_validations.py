"""Validaciones reutilizables para los datos de países."""


def validate_required_text(value, field_name="El campo"):
    """Devuelve el texto limpio o genera un error si está vacío."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} es obligatorio.")
    return value.strip()


def validate_positive_number(value, field_name="El valor", number_type=float):
    """Convierte y valida un número mayor que cero."""
    try:
        number = number_type(value)
    except (TypeError, ValueError) as error:
        type_name = "entero" if number_type is int else "número"
        raise ValueError(f"{field_name} debe ser un {type_name} válido.") from error

    if number <= 0:
        raise ValueError(f"{field_name} debe ser mayor que cero.")
    return number


def validate_country_data(country):
    """Valida y normaliza un diccionario que representa un país."""
    if not isinstance(country, dict):
        raise ValueError("Los datos del país no son válidos.")

    return {
        "name": validate_required_text(country.get("name"), "El nombre"),
        "continent": validate_required_text(
            country.get("continent"), "El continente"
        ),
        "population": validate_positive_number(
            country.get("population"), "La población", int
        ),
        "area": validate_positive_number(country.get("area"), "La superficie", float),
    }


def validate_range(minimum, maximum, field_name, number_type=float):
    """Valida los extremos positivos de un rango."""
    minimum = validate_positive_number(minimum, f"{field_name} mínima", number_type)
    maximum = validate_positive_number(maximum, f"{field_name} máxima", number_type)
    if minimum > maximum:
        raise ValueError(f"{field_name} mínima no puede superar a la máxima.")
    return minimum, maximum
