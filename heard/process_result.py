def process_first_result(search_result):
    try:
        # Divide el resultado en líneas
        lines = search_result.split('\n')

        # Verifica que haya suficientes líneas para procesar
        if len(lines) >= 3:
            # Extrae la URL del segundo elemento
            url = lines[1].strip()

            # Extrae las posiciones del tercer elemento, dividiendo por '·'
            positions = lines[2].strip().split('·')

            # Limpia espacios en blanco adicionales en cada posición
            positions = [position.strip() for position in positions]

            print(f"URL: {url}")
            return url, positions
        else:
            # Si el formato no es el esperado, retorna None
            return None, None
    except Exception as e:
        print(f"Error procesando el resultado: {e}")
        return None, None
