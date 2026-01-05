import csv
import json
import time
from hashlib import sha256

DEFAULT_DESCRIPTION = 'Descripción no disponible'
DEFAULT_PICURL = 'https://example.com/default-pic.png'
DEFAULT_CATEGORY_PICURL = 'https://example.com/default-category-pic.png'

def extract_location(investment_name):
    """Extrae la ubicación del nombre de la inversión."""
    # Buscar patrones específicos en el nombre de la inversión
    if 'DISTRITO' in investment_name.upper():
        parts = investment_name.upper().split('DISTRITO')
        if len(parts) > 1:
            return parts[1].split(',')[0].strip()
    elif 'PROVINCIA' in investment_name.upper():
        parts = investment_name.upper().split('PROVINCIA')
        if len(parts) > 1:
            return parts[1].split(',')[0].strip()
    return 'AREQUIPA'  # Valor predeterminado

def generate_id(name):
    """Genera un ID único basado en el nombre y un timestamp."""
    timestamp = str(int(time.time() * 1000))
    unique_string = name + timestamp
    return 'proj_' + sha256(unique_string.encode()).hexdigest()[:8]

def generate_category_id(category_name):
    """Genera un ID único para cada categoría basada en su nombre."""
    return sha256(category_name.encode()).hexdigest()[:8]

def calculate_progress(devengado_acumulado, costo_actualizado):
    """Calcula el avance como (Devengado acumulado / Costo actualizado) × 100."""
    try:
        devengado = float(devengado_acumulado)
        costo = float(costo_actualizado)
        if costo > 0:
            return round((devengado / costo) * 100, 2)
    except ValueError:
        pass
    return 0.0

def csv_to_json_with_structure(csv_file, json_file):
    """Convierte datos de un CSV a un archivo JSON con la estructura de Firebase."""
    data = {
        'Category': [],
        'Projects': {}
    }

    category_map = {}

    # Leer el archivo CSV
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Procesar categorías dinámicamente
            funcion = row['FUNCION'].strip()
            if funcion not in category_map:
                category_id = generate_category_id(funcion)
                category_map[funcion] = {
                    'id': category_id,
                    'picUrl': DEFAULT_CATEGORY_PICURL,
                    'title': funcion
                }

            # Calcular avance
            avance = calculate_progress(row['DEVENGADO ACUMULADO'], row['COSTO ACTUALIZADO'])

            # Crear proyecto
            project_id = generate_id(row['NOMBRE DE LA INVERSION'])
            transformed_row = {
                'avance': avance,
                'categoryId': category_map[funcion]['id'],
                'cui': row['CUI'].strip() if row['CUI'] else '',
                'createdAt': int(time.time() * 1000),
                'description': DEFAULT_DESCRIPTION,
                'id': project_id,
                'name': row['NOMBRE DE LA INVERSION'],
                'picUrl': DEFAULT_PICURL,
                'presupuesto': float(row['MONTO VIABLE']) if row['MONTO VIABLE'] else 0,
                'ubicacion': extract_location(row['NOMBRE DE LA INVERSION'])
            }
            data['Projects'][project_id] = transformed_row

    # Agregar categorías al JSON
    data['Category'] = list(category_map.values())

    # Guardar en un archivo JSON
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    CSV_INPUT = 'data/arequipa/inversiones_arequipa.csv'
    JSON_OUTPUT = 'data/arequipa/inversiones_arequipa.json'

    csv_to_json_with_structure(CSV_INPUT, JSON_OUTPUT)
    print(f"Datos guardados en {JSON_OUTPUT}")