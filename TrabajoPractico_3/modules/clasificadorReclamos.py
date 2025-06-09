#dependencias
import pickle
import nltk

class ClasificadorDeReclamos:
    def __init__(self):
        with open('./data/claims_clf.pkl', 'rb') as archivo:
            self.clf = pickle.load(archivo)

    def clasificar(self, reclamos):
        if isinstance(reclamos, str):
            reclamos = [reclamos]
        reclamoClasificado = self.clf.clasificar(reclamos)
        return reclamoClasificado[0] #para devolver el 1er elemento

# Uso de la clase
if __name__ == "__main__":
    clasificador = ClasificadorDeReclamos()

    reclamos = [
        "La computadora 1 del laboratorio 3 no enciende", 
        "El proyector del aula 2 no proyecta la imagen", 
        "El piso del aula 5 está muy sucio", 
        "No puedo enviar mi trabajo por correo electrónico porque la red no funciona",
        "El pizarrón del aula 4 está roto",
        "La impresora de la biblioteca no imprime",
        "El aire acondicionado del aula 1 no enfría",
        "El baño de la planta baja está inundado",
    ]

    # Clasificación de un único reclamo
    print(clasificador.clasificar(reclamos))
