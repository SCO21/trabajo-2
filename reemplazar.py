import re

def quitar_tildes(palabra):
    tildes = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'}
    return ''.join(tildes.get(char, char) for char in palabra)

def procesar_archivo(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        contenido = file.read()

    contenido_procesado = re.sub(r'(?<=\n)([a-zA-Záéíóúüñ]+)', lambda x: quitar_tildes(x.group()), contenido)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(contenido_procesado)

# Uso de la función
procesar_archivo('lema8.txt', 'lema8(2).txt')