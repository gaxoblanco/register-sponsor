import json
import os
import shutil
import process_result
import google_search

# Función para crear una copia de seguridad


def backup_file(file_path):
    backup_path = file_path + ".bak"
    shutil.copyfile(file_path, backup_path)


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

    # valido que la entrada aun no tenga la url de linkedin
    # compresion de listas
    batch = [entry for entry in batch if 'linkedin_url' not in entry]

    # Por cada entrada en el lote hago la busqueda en Google
    for entry in batch:
        # Valido si ya tiene la URL de LinkedIn si la tiene no ejecuto la busqueda
        if 'linkedin_url' in entry:
            continue

        # Valido que en el campo industry_en tenga la cadena de texto software, si no lo tiene no ejecuto la busqueda
        if 'software' not in entry.get('industry_en', '').lower():
            continue

        name = entry.get('name', '')

        # Realiza la búsqueda en Google
        search_term = f"{name} linkein - jobs"
        results = google_search.search(search_term, num=1)

        # print(results[0]['link'] + '/jobs')  # type: ignore
        if results:
            first_result = results[0]
            # title = first_result.get('title', '')
            link = first_result.get('link', '') + '/jobs'
            # valido que la url tenga /company/ para que sea la url de linkedin que espero
            if '/company/' not in link:
                continue

            # busco si la cadena de texto contiene //job, si es asi lo convierto a /jobs
            if '//job' in link:
                link = link.replace('//job', '/jobs')

            # Actualiza los datos en el diccionario
            entry['linkedin_url'] = link
            # entry['positions'] = positions

            # Valido que el campo logo_url tenga la cade de texto: https://index-edge.creditsafe.com, si es asi la reemplazo con el valor de entry['cse_image']


# Guarda los datos actualizados en un archivo temporal
    temp_file = input_file + '.tmp'
    try:
        with open(temp_file, 'w') as file:
            json.dump(data, file, indent=4)

        # Si la escritura fue exitosa, reemplaza el archivo original
        os.replace(temp_file, input_file)
    except Exception as e:
        print(f"Error guardando el archivo JSON: {e}")
        exit(1)

    print(f"Procesado el lote de {i} a {i + batch_size}")

print("Actualización completa.")
