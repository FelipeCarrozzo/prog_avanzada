import pickle
import nltk
# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

class ClasificadorDeReclamos:
    def __init__(self, ruta_modelo):
        self.ruta_modelo = ruta_modelo
        self.clf = self._cargar_modelo()

    def _cargar_modelo(self):
        with open(self.ruta_modelo, 'rb') as archivo:
            return pickle.load(archivo)

    def clasificar(self, reclamos):
        return self.clf.clasificar(reclamos)


# Uso de la clase
if __name__ == "__main__":
    ruta_modelo = './data/claims_clf.pkl'
    clasificador = ClasificadorDeReclamos(ruta_modelo)

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

    # Clasificación de múltiples reclamos
    # print(clasificador.clasificar(reclamos))

    # Clasificación de un único reclamo
    print(clasificador.clasificar(["El proyector del aula 2 no proyecta la imagen"]))
