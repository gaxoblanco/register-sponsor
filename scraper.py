import requests
from bs4 import BeautifulSoup, Tag
import json

# URL de la página web que contiene la tabla
url = 'https://ind.nl/en/public-register-recognised-sponsors/public-register-regular-labour-and-highly-skilled-migrants'

# Realiza una solicitud GET a la URL
response = requests.get(url)

# Verifica que la solicitud fue exitosa
if response.status_code == 200:
    # Analiza el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encuentra la primera etiqueta <table> en el HTML
    table = soup.find('table')

    # Inicializa una lista para almacenar los datos de la tabla
    data = []

    # Verifica que se encontró una tabla
    if table:
        # Encuentra todas las filas <tr> en la tabla
        rows = table.find_all('tr')  # type: ignore

        # Verifica que existen filas en la tabla
        if rows:
            # Itera sobre las filas, saltando la primera (cabecera)
            for row in rows[1:]:
                # Encuentra todas las celdas <td> en la fila
                cols = row.find_all('td')

                # Verifica que la fila contiene al menos dos celdas
                if len(cols) >= 2:
                    # Extrae los valores de texto de cada celda
                    organisation = cols[0].text.strip()
                    kvk_number = cols[1].text.strip()

                    # Agrega un diccionario con los datos a la lista
                    data.append({
                        'name': organisation,
                        'id': kvk_number
                    })

    # Convierte la lista de diccionarios a una cadena JSON
    json_data = json.dumps(data, indent=4)

    # Define el nombre del archivo JSON
    output_file = 'sponsors.json'

    # Guarda los datos en un archivo JSON
    with open(output_file, 'w') as file:
        file.write(json_data)

    # Imprime un mensaje de éxito
    print(f"Datos guardados en {output_file}")
else:
    print(f"Error al acceder a la página: {response.status_code}")
