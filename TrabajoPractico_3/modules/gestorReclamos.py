from modules.reclamo import Reclamo
# from modules.usuario import Usuario
from modules.gestorUsuarios import GestorUsuarios
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from modules.factoriaRepositorios import crearRepositorio
from modules.clasificadorReclamos import ClasificadorDeReclamos
import datetime
# import re
# from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from modules.clasificadorReclamos import ClasificadorDeReclamos


class GestorReclamos:
    def __init__(self, repo: RepositorioAbstractoBD):
        self.__repo = repo
        self.__clasificador = ClasificadorDeReclamos()
        self.__departamentos = []
        

    @property
    def clasificador(self):
        """Devuelve el clasificador de reclamos."""
        return self.__clasificador
    
    @property
    def departamentos(self):
        """Devuelve la lista de departamentos."""
        return self.__departamentos
    
    def verificarReclamoExistente(self, idUsuario, descripcion):
        #verifico si ya existe recorriendo todos los reclamos del usuario
        try:
            reclamosUsuario = self.__repo.obtenerRegistrosFiltro("idUsuario", idUsuario)
            for reclamo in reclamosUsuario:
                if reclamo.descripcion == descripcion:
                    raise ValueError("El reclamo ya está registrado.")
        except ValueError as e:
            print(f"Error al verificar si existe el reclamo: {e}")

        #busco reclamos similares
        try:
            reclamosSimilares = self.obtenerReclamosSimilares(descripcion)
            if reclamosSimilares:
                return reclamosSimilares
            return None
        except Exception as e:
            print(f"Error al obtener reclamos similares: {e}")

    def crearReclamo(self, idUsuario, descripcion, imagen):
        try:
            #clasifico el reclamo
            departamentoReclamo = self.__clasificador.clasificar([descripcion])
        except Exception as e:
            print(f"Error al clasificar el reclamo: {e}")
        
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

            self.__repo.guardarRegistro(reclamo)  # Guardar en el repositorio
            print(f"Reclamo creado con éxito: {reclamo.to_dict()}")
        except Exception as e:
            print(f"Error al guardar el reclamo en BD: {e}")


    def clasificarReclamo(self, descripcion: str):
        self.__clasificador.clasificar([descripcion])


    def adherirAReclamo(self, id, usuario):
        """Adhiere un usuario a un reclamo existente."""
        reclamo = self.__repo.obtenerRegistroFiltro("id", id)
        if reclamo:
            if usuario not in reclamo.usuariosAdheridos:
                self.__repo.agregarUsuarioAReclamo(reclamo.id, usuario)
                return True
        return False


    def guardarReclamo(self, reclamo):
        #guardo en el repositorio
        self.__repo.guardarRegistro(reclamo.to_dict())

    
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
        clasificacion = self.__clasificador.clasificar([desc_nueva])

        candidatos = self.__repo.obtenerRegistrosFiltro("departamento", clasificacion)
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
          
        # return [r.descripcion for r, _ in similares]
        return [{"id": r.id, "descripcion": r.descripcion} for r, _ in similares]
    
if __name__ == "__main__":
    # Ejemplo de uso
    repoUsuario, repoReclamo = crearRepositorio()
    gestorR = GestorReclamos(repoReclamo)
    gestorU = GestorUsuarios(repoUsuario)
    #necesito
    # usuario = repoUsuario.obtenerRegistroFiltro("id", 4)

    # #similar
    # similar = gestorR.verificarReclamoExistente(1, "El dispenser del agua caliente no funciona correctamente.")
    # print(similar)

    # #adherir
    # adhesion = gestorR.adherirAReclamo(1, usuario)  # idReclamo, idUsuario
    # if adhesion:
    #     print("Usuario adherido al reclamo.")
    # else:
    #     print("No se pudo adherir al reclamo.")

    # similares = gestor.obtenerReclamosSimilares({'descripcion': "El dispenser del agua caliente no funciona correctamente."})
    # print(similares)

    #elimino la tabla Reclamos
    # repoUsuario.borrarTabla("Usuarios")
    # repoReclamo.borrarTabla("Reclamos")