from collections import defaultdict

def contar_frases(nombre_archivo):
    conteo_peliculas = defaultdict(int)  # Diccionario con valores por defecto en 0

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(";")
            if len(partes) == 2:
                pelicula = partes[1].strip()
                conteo_peliculas[pelicula] += 1  # Incrementa el contador de la película

    return conteo_peliculas

# Llamada a la función con el archivo de frases
conteo = contar_frases("data/frases_de_peliculas.txt")

# Mostrar resultados ordenados alfabéticamente
for pelicula, cantidad in sorted(conteo.items()):
    print(f"{pelicula}: {cantidad} frases")
