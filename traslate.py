import json
from transformers import pipeline

# Cargar el modelo de traducción de neerlandés a inglés
traductor = pipeline("translation", model="Helsinki-NLP/opus-mt-nl-en")


def traducir(texto):
    resultado = traductor(texto, max_length=512)
    return resultado[0]['translation_text']  # type: ignore


def procesar_sponsors(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r', encoding='utf-8') as file_in, \
            open(archivo_salida, 'w', encoding='utf-8') as file_out:

        # Leer todo el JSON
        sponsors = json.load(file_in)

        # Escribir el inicio del array JSON
        file_out.write('[\n')

        for i, sponsor in enumerate(sponsors):
            # Eliminar el campo 'company_info'
            sponsor.pop('company_info', None)

            if 'industry' in sponsor:
                industry_nl = sponsor['industry']
                industry_en = traducir(industry_nl)
                sponsor['industry_en'] = industry_en
                print(
                    f"Sponsor: {sponsor.get('name', 'Nombre no disponible')}")
                print(f"Industry (Dutch): {industry_nl}")
                print(f"Industry (English): {industry_en}")
                print("-" * 40)
            else:
                print(
                    f"Sponsor: {sponsor.get('name', 'Nombre no disponible')} - No industry found")
                print("-" * 40)

            # Escribir el sponsor actualizado en el archivo de salida
            json.dump(sponsor, file_out, ensure_ascii=False, indent=4)

            # Añadir coma si no es el último elemento
            if i < len(sponsors) - 1:
                file_out.write(',\n')
            else:
                file_out.write('\n')

        # Escribir el final del array JSON
        file_out.write(']')


# Ejecutar el procesamiento
procesar_sponsors('sponsors.json', 'sponsors_updated.json')

print("El archivo JSON ha sido actualizado y guardado como 'sponsors_updated.json'")
