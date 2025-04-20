from modules.persona import Persona

class Profesor(Persona):
    def __init__(self, nombre, apellido, dni):
        super().__init__(nombre, apellido, dni)
        self.__departamentos = []

    def asociar_departamento(self, depto):
        if depto not in self.__departamentos:
            self.__departamentos.append(depto)

    def __str__(self):
        return super().__str__()
