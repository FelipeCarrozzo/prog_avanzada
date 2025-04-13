class Profesor:
    def __init__(self, nombre, apellido, dni):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__departamentos = []

    def asociar_departamento(self, depto):
        if depto not in self.__departamentos:
            self.__departamentos.append(depto)

    def __str__(self):
        return f"{self.__nombre} {self.__apellido}, DNI: {self.__dni}"