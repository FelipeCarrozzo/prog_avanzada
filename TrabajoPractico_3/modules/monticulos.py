class MonticuloBinario:
    """
    Clase que representa un montículo binario.
    Permite insertar elementos y mantener la propiedad de montículo (min o max).
    """
    def __init__(self, tipo):
        self.__listaValores = [None]
        self.__tamanioActual = 0
        self.__tipo = tipo #"min" o "max"

    @property
    def tamanioActual(self):
        return self.__tamanioActual

    def devolverListaValores(self):
        """
        Devuelve una copia de la lista de valores del montículo.
        """
        return self.__listaValores.copy()

    def infiltrarArriba(self, valor):
        '''
        Mueve el elemento en la posición i hacia arriba en el montículo
        hasta que se cumpla la propiedad del montículo.
        args:
        valor: El índice del elemento a mover hacia arriba.
        '''
        if self.__tipo == "min":
            while valor // 2 > 0:
                if self.__listaValores[valor] < self.__listaValores[valor // 2]:
                    tmp = self.__listaValores[valor // 2]
                    self.__listaValores[valor // 2] = self.__listaValores[valor]
                    self.__listaValores[valor] = tmp
                valor = valor // 2
        elif self.__tipo == "max":
           while valor // 2 > 0:
                if self.__listaValores[valor] > self.__listaValores[valor // 2]:
                    tmp = self.__listaValores[valor // 2]
                    self.__listaValores[valor // 2] = self.__listaValores[valor]
                    self.__listaValores[valor] = tmp
                valor = valor // 2

    def infiltrarAbajo(self, valor):
        '''
        Mueve el elemento en la posición i hacia abajo en el montículo
        hasta que se cumpla la propiedad del montículo.
        args:
        valor: El índice del elemento a mover hacia abajo.
        ''' 
        if self.__tipo == "min":
            while (valor * 2) <= self.__tamanioActual:
                hm = self.hijoMinOMax(valor)
                if self.__listaValores[valor] > self.__listaValores[hm]:
                    tmp = self.__listaValores[valor]
                    self.__listaValores[valor] = self.__listaValores[hm]
                    self.__listaValores[hm] = tmp
                valor = hm
        elif self.__tipo == "max":
            while (valor * 2) <= self.__tamanioActual:
                hm = self.hijoMinOMax(valor)
                if self.__listaValores[valor] < self.__listaValores[hm]:
                    tmp = self.__listaValores[valor]
                    self.__listaValores[valor] = self.__listaValores[hm]
                    self.__listaValores[hm] = tmp
                valor = hm

    def insertar(self, valor):
        """
        Inserta un nuevo elemento en el montículo.
        args:
        valor: El valor a insertar en el montículo.
        """
        self.__listaValores.append(valor)
        self.__tamanioActual = self.__tamanioActual + 1
        self.infiltrarArriba(self.__tamanioActual)

    def hijoMinOMax(self, valor):
        """
        Devuelve el índice del hijo mínimo o máximo de un nodo dado.
        args:
        valor: El índice del elemento padre.
        """
        if valor * 2 + 1 > self.__tamanioActual:
            return valor * 2
        else:
            if self.__tipo == 'min':
                if self.__listaValores[valor * 2] < self.__listaValores[valor * 2 + 1]:
                    return valor * 2
                else:
                    return valor * 2 + 1
            else:
                if self.__listaValores[valor * 2] > self.__listaValores[valor * 2 + 1]:
                    return valor * 2
                else:
                    return valor * 2 + 1

    def eliminarMinOMax(self):
        '''
        Elimina el elemento mínimo o máximo del montículo y lo devuelve.
        '''
        if self.__tamanioActual == 0:
            raise IndexError("El montículo está vacío.")
        raiz = self.__listaValores[1]
        self.__listaValores[1] = self.__listaValores[self.__tamanioActual]
        self.__tamanioActual = self.__tamanioActual - 1
        self.__listaValores.pop()
        self.infiltrarAbajo(1)
        return raiz

class MonticuloMediana:
    def __init__(self):
      self.__monticuloMin = MonticuloBinario("min")
      self.__monticuloMax = MonticuloBinario("max")
    
    def agregarValor(self, valor: int):
        """
        Agrega un nuevo valor al montículo de mediana.
        Dependiendo del valor, se inserta en el montículo mínimo o máximo.
        Luego, se balancean los montículos para mantener la propiedad de mediana.
        args:
        valor: El valor a agregar al montículo.
        """
        if self.__monticuloMin.tamanioActual == 0 and self.__monticuloMax.tamanioActual == 0:
            self.__monticuloMin.insertar(valor)
        else:
            mediana_actual = self.obtenerMediana()
            if valor > mediana_actual:
                self.__monticuloMin.insertar(valor)
            else:
                self.__monticuloMax.insertar(valor)

        # Balancear los montículos
        if self.__monticuloMin.tamanioActual > self.__monticuloMax.tamanioActual + 1:
            valorSacado = self.__monticuloMin.eliminarMinOMax()
            self.__monticuloMax.insertar(valorSacado)
        elif self.__monticuloMax.tamanioActual > self.__monticuloMin.tamanioActual:
            valorSacado = self.__monticuloMax.eliminarMinOMax()
            self.__monticuloMin.insertar(valorSacado)
    
    def obtenerMediana(self) -> float:
        """
        Obtiene la mediana de los valores agregados al montículo.
        Si los montículos están vacíos, lanza una excepción.
        """
        if self.__monticuloMin.tamanioActual == 0 and self.__monticuloMax.tamanioActual == 0:
            raise IndexError("No hay valores para calcular la mediana.")
        
        if self.__monticuloMin.tamanioActual > self.__monticuloMax.tamanioActual:
            return self.__monticuloMin.devolverListaValores()[1]
        elif self.__monticuloMin.tamanioActual < self.__monticuloMax.tamanioActual:
            return self.__monticuloMax.devolverListaValores()[1]
        else:
            return (self.__monticuloMin.devolverListaValores()[1] + self.__monticuloMax.devolverListaValores()[1]) / 2