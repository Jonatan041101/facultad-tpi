"""Persistencia de países en un archivo CSV."""

import csv
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "data", "paises.csv")
FIELDNAMES = ["name", "continent", "population", "area"]


def ensure_csv_exists(file_path=DEFAULT_CSV_PATH):
    """Crea la carpeta y un CSV con encabezados cuando todavía no existen."""
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_countries(file_path=DEFAULT_CSV_PATH):
    """Carga el CSV y convierte cada fila en un diccionario de país."""
    ensure_csv_exists(file_path)
    countries = []

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDNAMES:
            raise ValueError(
                "El CSV debe contener las columnas: " + ", ".join(FIELDNAMES)
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                countries.append({
                    "name": row["name"].strip(),
                    "continent": row["continent"].strip(),
                    "population": int(row["population"]),
                    "area": float(row["area"]),
                })
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Datos inválidos en la fila {row_number} del CSV."
                ) from error

    return countries


def save_countries(countries, file_path=DEFAULT_CSV_PATH):
    """Sobrescribe el CSV con el contenido actual de la lista de países."""
    ensure_csv_exists(file_path)

    with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(countries)
