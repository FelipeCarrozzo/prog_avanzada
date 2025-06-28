#dependencias
import pickle
import nltk

class ClasificadorDeReclamos:
    """
    Clase para clasificar reclamos en diferentes categorías.
    Utiliza un modelo previamente entrenado y guardado en un archivo pickle.
    """
    def __init__(self):
        with open('./data/claims_clf.pkl', 'rb') as archivo:
            self.clf = pickle.load(archivo)

    def clasificar(self, reclamo):
        """
        Clasifica un reclamo o una lista de reclamos.
        reclamo: str o list[str] - Descripción del reclamo o lista de descripciones.
        Devuelve la categoría del reclamo.
        """
        if isinstance(reclamo, str):
            reclamo = [reclamo]
        reclamoClasificado = self.clf.clasificar(reclamo)
        return reclamoClasificado[0] #para devolver el 1er elemento