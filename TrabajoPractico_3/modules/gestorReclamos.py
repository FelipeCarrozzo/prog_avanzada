from modules.reclamo import Reclamo
from modules.repositorioAbstractoBD import RepositorioAbstractoBD
from modules.clasificadorReclamos import ClasificadorDeReclamos


class GestorReclamos:
    def __init__(self, repo: RepositorioAbstractoBD):
        self.__repo = repo
        self.__reclamos = [] #lista de diccionarios
        # self.__clasificador = ClasificadorDeReclamos()
        self.__departamentos = []

    @property
    def reclamos(self):
        """Devuelve la lista de reclamos."""
        return self.__reclamos
    
    @property
    def departamentos(self):
        """Devuelve la lista de departamentos."""
        return self.__departamentos

    def crearReclamo(self, idReclamo, fechaYHora, estado, tiempoResolucion,
                    usuarioCreador, numeroAdheridos, usuariosAdheridos, descripcion, imagen): #saco el depto y lo agrego despues de la clasif
        
        # Verifica si el reclamo ya existe
        if self.__repo.obtenerRegistroFiltro("idReclamo", idReclamo):
            raise ValueError("El reclamo ya está registrado.")

        else:
            #clasifica el reclamo y guarda ese resultado como valor de departamento
            """puede ser que el tipo de dato no esté bien"""
            departamentoClasif = self.clasificarReclamo(descripcion)

            #Crea una instancia de Reclamo
            reclamo = Reclamo(idReclamo, fechaYHora, estado, tiempoResolucion, departamentoClasif,
                            usuarioCreador, numeroAdheridos, usuariosAdheridos, descripcion, imagen)
            #busca reclamos similares
            self.buscarReclamoSimilar(reclamo)

            #guarda el reclamo en el repositorio y también en la lista de reclamos
            self.guardarReclamo(reclamo.to_dict())

        return reclamo

    def clasificarReclamo(self, descripcion: str):
        self.__clasificador.clasificar([descripcion])

    def buscarReclamoSimilar(self, reclamo):
        """Busca reclamos similares en el repositorio."""
        # Implementar lógica de búsqueda de reclamos similares
        pass

    def adherirAReclamo(self, id_reclamo, usuario):
        """Adhiere un usuario a un reclamo existente."""
        for reclamo in self.reclamos:
            if reclamo['id'] == id_reclamo:
                if usuario not in reclamo['usuariosAdheridos']:
                    reclamo['usuariosAdheridos'].append(usuario)
                    reclamo['numeroAdheridos'] += 1
                    return True
        return False
    

    def guardarReclamo(self, reclamo):
        #guardo en la lista de reclamos
        self.reclamos.append(reclamo.to_dict()) #lista

        #guardo en el repositorio
        self.__repo.guardarRegistro(reclamo.to_dict())


    def resolverReclamo(self, idReclamo, tiempoResolucion):
        """Marca un reclamo como resuelto y actualiza su tiempo de resolución."""
        for reclamo in self.reclamos:
            if reclamo['id'] == idReclamo:
                reclamo['estado'] = 'resuelto'
                reclamo['tiempoResolucion'] = tiempoResolucion
                return True
        return False

    def listarReclamos(self):
        return self.reclamos

    def devolverReclamo(self, idReclamo):
        for reclamo in self.reclamos:
            if reclamo['id'] == idReclamo:
                return reclamo
        return None

    """Estos métodos son necesarios?"""
    # def eliminarReclamo(self, id_reclamo):
    #     self.reclamos = [r for r in self.reclamos if r['id'] != id_reclamo]

    # def editarReclamo(self, id_reclamo, nuevo_reclamo):
    #     for i, reclamo in enumerate(self.reclamos):
    #         if reclamo['id'] == id_reclamo:
    #             self.reclamos[i] = nuevo_reclamo
    #             return True
    #     return False
