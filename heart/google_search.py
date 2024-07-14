from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Ahora puedes acceder a las variables de entorno usando os.getenv
API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def search(search_term, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=API_KEY)
        res = service.cse().list(q=search_term, cx=SEARCH_ENGINE_ID, **kwargs).execute()

        # print(f"Respuesta completa de la API: {res}")  # Para depuración

        if 'items' in res:
            return res['items']
        else:
            print("No se encontraron resultados.")
            return []
    except HttpError as e:
        print(f"Ocurrió un error al hacer la solicitud: {e}")
        return []


# Ejemplo de uso
results = search("3Dimerce B.V. linkein /jobs", num=1)

if results:
    for result in results:
        # Imprime el título del resultado
        print(result.get('title', 'No title available'))

        # Imprime el enlace del resultado
        print(result.get('link', 'No link available'))

        # Imprime la imagen, si está disponible
        # if 'cse_image' in result:
        #     print(result['cse_image'])
        # else:
        #     print('No image available')

        # Imprime el snippet, si está disponible
        print(result.get('snippet', 'No snippet available'))
        print()
else:
    print("No se pudieron obtener resultados. Verifica tus credenciales y configuración.")
