import json


def filter_positions(input_file, search_term):
    try:
        # Lee los datos del archivo JSON
        with open(input_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {input_file}")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo {input_file} no es un JSON válido")
        return []

    # Lista para almacenar las entradas que cumplen con el criterio de búsqueda
    filtered_entries = []

    # Itera sobre las entradas y verifica si la palabra buscada está en el subarray positions
    for entry in data:
        if 'positions' in entry:
            for position in entry['positions']:
                if search_term.lower() in position.lower():
                    filtered_entries.append(entry)
                    break  # No es necesario seguir buscando en este entry si ya encontramos el término

    return filtered_entries


# Ejemplo de uso
input_file = '../sponsors.json'
search_term = 'front-end'
filtered_entries = filter_positions(input_file, search_term)

# Imprimir resultados
for entry in filtered_entries:
    print(json.dumps(entry, indent=4))
