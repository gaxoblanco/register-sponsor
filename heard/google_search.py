from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Reemplaza con tus propias credenciales
API_KEY = "AIzaSyDgygjZC4w1Mik2Lj4w6X4ir6fxaSD0Q9s"
SEARCH_ENGINE_ID = "d32d95372b4d24e6a"


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
# results = search("3Dimerce B.V. linkein /jobs", num=1)

# if results:
#     for result in results:
#         print(result['title'])
#         print(result['link'])
#         print(result.get('snippet', 'No snippet available'))
#         print()
# else:
#     print("No se pudieron obtener resultados. Verifica tus credenciales y configuración.")
