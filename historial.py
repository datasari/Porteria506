from excepciones import ErrorPorteria


class NodoDoble:
    def __init__(self, dato, anterior=None, siguiente=None):
        self.__dato = dato
        self.__anterior = anterior
        self.__siguiente = siguiente

    @property
    def dato(self):
        return self.__dato

    @property
    def anterior(self):
        return self.__anterior

    @anterior.setter
    def anterior(self, nodo):
        self.__anterior = nodo

    @property
    def siguiente(self):
        return self.__siguiente

    @siguiente.setter
    def siguiente(self, nodo):
        self.__siguiente = nodo


class Historial:
    def __init__(self):
        self.__cabeza = None
        self.__cola = None
        self.__tamano = 0

    @property
    def cabeza(self):
        return self.__cabeza

    @property
    def cola(self):
        return self.__cola

    def esta_vacia(self):
        return self.__cabeza is None

    def cantidad(self):
        return self.__tamano

    def agregar(self, paquete):
        nuevo = NodoDoble(paquete, self.__cola, None)
        if self.esta_vacia():
            self.__cabeza = nuevo
        else:
            self.__cola.siguiente = nuevo
        self.__cola = nuevo
        self.__tamano += 1

    def quitar_ultimo(self):
        if self.esta_vacia():
            raise ErrorPorteria("El historial está vacío")
        dato = self.__cola.dato
        self.__cola = self.__cola.anterior
        if self.__cola is None:
            self.__cabeza = None
        else:
            self.__cola.siguiente = None
        self.__tamano -= 1
        return dato

    def recientes(self, cantidad):
        texto = ""
        actual = self.__cola
        contador = 0
        while actual is not None and contador < cantidad:
            texto += f"{contador + 1}. {actual.dato.guia} - "
            texto += f"{actual.dato.recibido_por}\n"
            actual = actual.anterior
            contador += 1
        return texto.rstrip("\n")

    def de_apartamento(self, bloque, numero):
        resultado = Historial()
        actual = self.__cabeza
        while actual is not None:
            destino = actual.dato.destino
            if destino.bloque.nombre == str(bloque) and \
                    destino.numero == int(numero):
                resultado.agregar(actual.dato)
            actual = actual.siguiente
        return resultado

    def __str__(self):
        if self.esta_vacia():
            return "Historial vacío"
        texto = ""
        actual = self.__cabeza
        posicion = 1
        while actual is not None:
            texto += f"{posicion}. {actual.dato}\n"
            actual = actual.siguiente
            posicion += 1
        return texto.rstrip("\n")
