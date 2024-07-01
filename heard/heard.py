import json
import os
import process_result
import google_search

# Define el nombre del archivo JSON de entrada
input_file = os.path.abspath('sponsors.json')

# Lee los datos del archivo JSON
try:
    with open(input_file, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: El archivo '{input_file}' no se encontró.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: El archivo '{input_file}' no es un JSON válido.")
    exit(1)

# --------------------------------------------------------

# Itera por cada entrada en el archivo JSON de a paquetes de a 10
batch_size = 10

for i in range(0, len(data), batch_size):
    batch = data[i:i + batch_size]

    # Por cada entrada en el lote hago la busqueda en Google
    for entry in batch:
        # Valido si ya tiene la URL de LinkedIn si la tiene no ejecuto la busqueda
        if 'linkedin_url' in entry:
            continue

        name = entry.get('name', '')

        # Realiza la búsqueda en Google
        search_term = f"{name} linkein - jobs"
        results = google_search.search(search_term, num=2)

        # print(results[0]['link'] + '/jobs')  # type: ignore
        # print('---------------->>---')
        if results:
            first_result = results[0]
            # title = first_result.get('title', '')
            link = first_result.get('link' + '/jobs', '')
            snippet = first_result.get('snippet', '')

            # Procesa el primer resultado
            url, positions = process_result.process_first_result(snippet)

            # Actualiza los datos en el diccionario
            entry['linkedin_url'] = url
            entry['positions'] = positions

    # Guarda los datos actualizados en un archivo JSON
    try:
        with open(input_file, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error guardando el archivo JSON: {e}")
        exit(1)

    print(f"Procesado el lote de {i} a {i + batch_size}")
