class MonticuloBinario:
    """
    Clase que representa un montículo binario.
    Permite insertar elementos y mantener la propiedad de montículo (min o max).
    """
    def __init__(self, pTipo):
        self.__listaValores = [None]
        self.__tamanioActual = 0
        self.__tipo = pTipo #"min" o "max"

    @property
    def tamanioActual(self):
        return self.__tamanioActual

    def devolverListaValores(self):
        return self.__listaValores.copy()

    def infiltrarArriba(self, valor):
        '''
        Mueve el elemento en la posición i hacia arriba en el montículo
        hasta que se cumpla la propiedad del montículo.
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

    def insertar(self,valor):
        """Inserta un nuevo elemento en el montículo.
        args:
        k: El valor a insertar en el montículo.
        """
        self.__listaValores.append(valor)
        self.__tamanioActual = self.__tamanioActual + 1
        self.infiltrarArriba(self.__tamanioActual)

    def hijoMinOMax(self, valor):
        """
        Devuelve el índice del hijo mínimo o máximo de i.
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
            raise ValueError("El montículo está vacío.")
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
        #si el valor es el primero, se agrega directamente al montículo mínimo
        #valor > obtenerMediana() -> se agrega al montículo mínimo
        #valor < obtenerMe diana() -> se agrega al montículo máximo
        # if self.__monticuloMax.tamanioActual == 0 or valor <= self.__monticuloMax.devolverListaValores()[1]:
        #     self.__monticuloMax.insertar(valor)
        # else:
        #     self.__monticuloMin.insertar(valor)
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
        if self.__monticuloMin.tamanioActual == 0 and self.__monticuloMax.tamanioActual == 0:
            raise ValueError("No hay valores para calcular la mediana.")
        
        if self.__monticuloMin.tamanioActual > self.__monticuloMax.tamanioActual:
            return self.__monticuloMin.devolverListaValores()[1]
        elif self.__monticuloMin.tamanioActual < self.__monticuloMax.tamanioActual:
            return self.__monticuloMax.devolverListaValores()[1]
        else:
            return (self.__monticuloMin.devolverListaValores()[1] + self.__monticuloMax.devolverListaValores()[1]) / 2