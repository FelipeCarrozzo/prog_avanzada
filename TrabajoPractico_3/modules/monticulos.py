class MonticuloBinario:
    def __init__(self, pTipo):
        self.__listaValores = [None]
        self.__tamanioActual = 0
        self.__tipo = pTipo #"min" o "max"

    def infiltrarArriba(self,i):
        '''
        Mueve el elemento en la posición i hacia arriba en el montículo
        hasta que se cumpla la propiedad del montículo.
        '''
        if self.__tipo == "min":
            while i // 2 > 0:
                if self.__listaValores[i] < self.__listaValores[i // 2]:
                    tmp = self.__listaValores[i // 2]
                    self.__listaValores[i // 2] = self.__listaValores[i]
                    self.__listaValores[i] = tmp
                i = i // 2
        elif self.__tipo == "max":
           while i // 2 > 0:
                if self.__listaValores[i] > self.__listaValores[i // 2]:
                    tmp = self.__listaValores[i // 2]
                    self.__listaValores[i // 2] = self.__listaValores[i]
                    self.__listaValores[i] = tmp
                i = i // 2

    def infiltrarAbajo(self,i):
        '''
        Mueve el elemento en la posición i hacia abajo en el montículo
        hasta que se cumpla la propiedad del montículo.
        ''' 
        if self.__tipo == "min":
            while (i * 2) <= self.__tamanioActual:
                hm = self.hijoMin(i)
                if self.__listaValores[i] > self.__listaValores[hm]:
                    tmp = self.__listaValores[i]
                    self.__listaValores[i] = self.__listaValores[hm]
                    self.__listaValores[hm] = tmp
                i = hm
        elif self.__tipo == "max":
            while (i * 2) <= self.__tamanioActual:
                hm = self.hijoMax(i)
                if self.__listaValores[i] < self.__listaValores[hm]:
                    tmp = self.__listaValores[i]
                    self.__listaValores[i] = self.__listaValores[hm]
                    self.__listaValores[hm] = tmp
                i = hm

    def insertar(self,k):
        self.__listaValores.append(k)
        self.__tamanioActual = self.__tamanioActual + 1
        self.infiltrarArriba(self.__tamanioActual)

    def hijoMinOMax(self,i):
        '''
        Devuelve el índice del hijo mínimo o máximo de i.
        '''
        if i * 2 + 1 > self.__tamanioActual:
            return i * 2
        else:
            if self.__listaValores[i*2] < self.__listaValores[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def eliminarMinOMax(self):
        '''
        Elimina el elemento mínimo o máximo del montículo y lo devuelve.
        '''
        if self.__tamanioActual == 0:
            raise ValueError("El montículo está vacío.")
        valorSacado = self.__listaValores[1]
        self.__listaValores[1] = self.__listaValores[self.__tamanioActual]
        self.__tamanioActual = self.__tamanioActual - 1
        self.__listaValores.pop()
        self.infiltrarAbajo(1)
        return valorSacado

    def devolverListaValores(self):
        return self.__listaValores.copy()


class MonticuloMediana:
    def __init__(self):
      self.__monticuloMin = MonticuloBinario("min")
      self.__monticuloMax = MonticuloBinario("max")
    
    def agregarValor(self, valor: int):
        #si el valor es el primero, se agrega directamente al montículo mínimo
        #valor > obtenerMediana() -> se agrega al montículo mínimo
        #valor < obtenerMediana() -> se agrega al montículo máximo
        if self.__monticuloMin.tamanioActual == 0 or valor < self.__monticuloMin.devolverListaValores()[1]: #si el valor es menor a la raiz
            self.__monticuloMin.insertar(valor)
        else:
            self.__monticuloMax.insertar(valor)

        # Balancear los montículos
        if self.__monticuloMin.tamanioActual > self.__monticuloMax.tamanioActual + 1:
            valorSacado = self.__monticuloMin.eliminarMinO
            self.__monticuloMax.insertar(valorSacado)
        elif self.__monticuloMax.tamanioActual > self.__monticuloMin.tamanioActual:
            valorSacado = self.__monticuloMax.eliminarMin()
            self.__monticuloMin.insertar(valorSacado)
    
    def obtenerMediana(self) -> float:
        if self.__monticuloMin.tamanioActual == 0 and self.__monticuloMax.tamanioActual == 0:
            raise ValueError("No hay valores para calcular la mediana.")
        
        if self.__monticuloMin.tamanioActual > self.__monticuloMax.tamanioActual:
            return self.__monticuloMin.listaMonticulo[1]
        elif self.__monticuloMin.tamanioActual < self.__monticuloMax.tamanioActual:
            return self.__monticuloMax.listaMonticulo[1]
        else:
            return (self.__monticuloMin.listaMonticulo[1] + self.__monticuloMax.listaMonticulo[1]) / 2

#operaciones:
#inicializar()
#agregarValor(valor)
#obtenerMediana(): float
#operacion eliminar() hace falta? spoiler: no. lo hace el montículo binario
