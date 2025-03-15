import os

peliculas = set()  # conjunto para evitar duplicados

with open('data/frases_de_peliculas.txt', "r", encoding="utf-8") as archivo:
    for linea in archivo:
        partes = linea.strip().split(";")
        if len(partes) == 2:  # si tiene dos datos por linea
            pelicula = partes[1].strip() 
            peliculas.add(pelicula) # guardo en pelicula y la guardo en peliculas

lista_ordenada = sorted(peliculas)

# Imprimir lista indexada con enumerate (con dos variables)
for i, pelicula in enumerate(lista_ordenada, start=1): #start1 para que empiece en 1 el indexado
    print(f"{i}. {pelicula}")

# carpeta para guardar el archivo
carpeta = "data" 

# Ruta completa
ruta_archivo = os.path.join(carpeta, "peliculas_indexadas.txt")

# Lista por comprension. Itera sobre la lista_ordenada con el formato "i. pelicula"
lista_indexada = [f"{i}. {pelicula}" for i, pelicula in enumerate(lista_ordenada, start=1)]

# Guardo lista_indexada en la carpeta 'data'
with open(ruta_archivo, "w", encoding="utf-8") as archivo:
    archivo.write("\n".join(lista_indexada))