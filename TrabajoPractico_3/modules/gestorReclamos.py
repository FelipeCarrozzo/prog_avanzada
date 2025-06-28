#dependencias
from modules.reclamo import Reclamo
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from modules.clasificadorReclamos import ClasificadorDeReclamos
import datetime
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from modules.clasificadorReclamos import ClasificadorDeReclamos

class GestorReclamos:
    """
    Clase para gestionar los reclamos en la aplicación.
    Permite crear, clasificar y adherir usuarios a reclamos.
    """
    def __init__(self, repositorio: RepositorioAbstractoBD):
        self.__repositorio = repositorio
        self.__clasificador = ClasificadorDeReclamos()

    def verificarReclamoExistente(self, idUsuario, descripcion):
        """
        Verifica si un reclamo ya existe para un usuario dado.
        Si el reclamo ya existe, lanza ValueError.
        Si no, devuelve una lista de reclamos similares (puede ser vacía).
        """
        reclamosUsuario = self.__repositorio.obtenerRegistrosFiltro("idUsuario", idUsuario)
        for reclamo in reclamosUsuario:
            if reclamo.descripcion == descripcion:
                raise ValueError("El reclamo ya está registrado.")

        reclamosSimilares = self.obtenerReclamosSimilares({"descripcion": descripcion})
        return reclamosSimilares
    
    def crearReclamo(self, idUsuario, descripcion, imagen):
        """
        Crea un nuevo reclamo para un usuario dado.
        """
        try:
            #clasifico el reclamo
            departamentoReclamo = self.clasificarReclamo(descripcion)
        except Exception as e:
            raise ValueError(f"Error al clasificar el reclamo: {e}")
        
        #creo la instancia de reclamo y la guardo en el repositorio
        try:
            reclamo = Reclamo(
                id = None,
                idUsuario = idUsuario,
                fechaYHora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                estado = 'pendiente',
                tiempoResolucion = None,
                departamento = departamentoReclamo,
                numeroAdheridos = 0,
                descripcion = descripcion,
                imagen = imagen,
                usuariosAdheridos = []
            )

            self.__repositorio.guardarRegistro(reclamo)  # Guardar en el repositorio
        except Exception as e:
            raise ValueError(f"Error al guardar el reclamo en BD: {e}")

    def clasificarReclamo(self, descripcion: str):
        """
        Clasifica un reclamo dado su descripción.
        descripcion: str - Descripción del reclamo a clasificar.
        Devuelve la categoría del reclamo.
        """
        return self.__clasificador.clasificar([descripcion])

    def adherirAReclamo(self, idReclamo, usuario):
        """
        Adhiere un usuario a un reclamo existente.
        """
        return(self.__repositorio.agregarUsuarioAReclamo(idReclamo, usuario))

    def obtenerReclamosSimilares(self, datosNuevoReclamo):
        """
        datos_reclamo: dict con al menos {'descripcion': str} #usar reclamos atributos?
        Devuelve lista de Reclamo (objetos) parecidos.
        """
        umbral = 0.3
        stop_words = set(stopwords.words('spanish'))

        def tokenizar(texto):
            tokens = word_tokenize(texto.lower())
            return [t for t in tokens if t.isalpha() and t not in stop_words]

        desc_nueva = datosNuevoReclamo['descripcion']
        tokens_nuevo = set(tokenizar(desc_nueva))
        # clasificamos el nuevo reclamo
        clasificacion = self.clasificarReclamo(desc_nueva)

        candidatos = self.__repositorio.obtenerRegistrosFiltro("departamento", clasificacion)
        candidatos = [r for r in candidatos if r.estado != 'resuelto']

        similares = []
        for r in candidatos:
            tokens_r = set(tokenizar(r.descripcion))
            # similaridad Jaccard
            inter = tokens_nuevo & tokens_r
            union = tokens_nuevo | tokens_r
            score = len(inter) / len(union) if union else 0
            if score >= umbral:
                similares.append((r, score))

        # ordeno de mayor a menor parecido y devuelvo sólo los objetos
        similares.sort(key=lambda x: x[1], reverse=True)
          
        return [{"id": r.id, "descripcion": r.descripcion} for r, _ in similares]