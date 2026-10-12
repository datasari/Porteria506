class ErrorPorteria(Exception):
    pass

class SinPendientes(ErrorPorteria):
    def __init__(self, mensaje="No hay pendientes por atender"):
        super().__init__(mensaje)

class CamionVacio(ErrorPorteria):
    def __init__(self, mensaje="El camión esta vacío"):
        super().__init__(mensaje)

class Nodo:
    def __init__(self, dato, siguiente = None):
        self.__dato = dato
        self.__siguiente = siguiente

    @property
    def dato(self):
        return self.__dato

    @property
    def siguiente(self):
        return self.__siguiente

    @siguiente.setter
    def siguiente(self, nodo):
        self.__siguiente = nodo

class ListaPaquetes:
    def __init__(self):
        self.__cabeza = None
        self.__ultimo = None
        self.__tamano = 0

    @property
    def cabeza(self):
        return self.__cabeza

    def esta_vacia(self):
        return self.__cabeza is None

    def cantidad(self):
        return self.__tamano
    
    def agregar(self, paquete): 
        nuevo = Nodo(paquete)
        if self.esta_vacia():
            self.__cabeza = nuevo
        else:
            self.__ultimo.siguiente = nuevo
        self.__ultimo = nuevo
        self.__tamano += 1
 
    def buscar(self, guia): 
        actual = self.__cabeza
        while actual is not None:
            if actual.dato.guia == guia:
                return actual.dato
            actual = actual.siguiente
        return None
 
    def quitar(self, guia): 
        anterior = None
        actual = self.__cabeza
        while actual is not None and actual.dato.guia != guia:
            anterior = actual
            actual = actual.siguiente
        if actual is None:     
            raise SinPendientes(f"la guía {guia} no está en la lista")
        if anterior is None: 
            self.__cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
        if actual is self.__ultimo:
            self.__ultimo = anterior
        self.__tamano -= 1 
        return actual.dato
    
    def quitar_primero(self): 
        if self.esta_vacia():
            raise SinPendientes("la lista está vacía")
        return self.quitar(self.__cabeza.dato.guia)

    def __str__(self): 
        if self.esta_vacia():
            return "Sin paquetes"
        texto = ""
        actual = self.__cabeza
        posicion = 1
        while actual is not None:
            texto += f"{posicion}. {actual.dato}\n"
            actual = actual.siguiente
            posicion += 1
        return texto.rstrip("\n")

class Cola:
    def __init__(self): 
        self.__frente = None
        self.__final = None
        self.__tamano = 0
 
    def esta_vacia(self):
        return self.__frente is None
 
    def cantidad(self):
        return self.__tamano
 
    def encolar(self, dato): 
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.__frente = nuevo
        else:
            self.__final.siguiente = nuevo
        self.__final = nuevo
        self.__tamano += 1
        
    def ver_frente(self): 
        if self.esta_vacia():
            raise CamionVacio()
        return self.__frente.dato
 
    def desencolar(self): 
        if self.esta_vacia():
            raise CamionVacio()
        dato = self.__frente.dato
        self.__frente = self.__frente.siguiente
        if self.__frente is None:
            self.__final = None
        self.__tamano -= 1
        return dato