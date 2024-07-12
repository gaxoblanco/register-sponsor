import json

# Función para analizar y extraer la URL de logo_clearbit y actualizar el campo company_url


def update_company_url(entry):
    clearbit_prefix = "https://logo.clearbit.com/"
    logo_url = entry.get('logo_url', '')

    if logo_url.startswith(clearbit_prefix):
        # Extrae la parte de la URL después de 'https://logo.clearbit.com/'
        extracted_url = logo_url[len(clearbit_prefix):]
        # Actualiza el campo company_url con la URL extraída
        entry['company_url'] = extracted_url
        return True
    return False


# Archivo JSON de entrada
input_file = 'sponsors.json'

# Leer los datos del archivo JSON
with open(input_file, 'r') as file:
    data = json.load(file)

# Itera por cada entrada en el archivo JSON y actualiza el campo company_url
for entry in data:
    if update_company_url(entry):
        print(
            f"Para la entrada con ID {entry['id']}, la URL extraída es: {entry['company_url']}")
    else:
        print(
            f"Para la entrada con ID {entry['id']}, no se encontró una URL de Clearbit.")

# Guarda los datos actualizados en el archivo JSON
try:
    with open(input_file, 'w') as file:
        json.dump(data, file, indent=4)
    print("El archivo JSON ha sido actualizado y guardado exitosamente.")
except Exception as e:
    print(f"Error guardando el archivo JSON: {e}")
