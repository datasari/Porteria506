from excepciones import ErrorPorteria 
from recepcion import Nodo

class PilaEntregas: 
   def __init__(self):
    self.__tope = None
    self.__tamano = 0 
    
    def esta_vacia(self): 
        return self.__tope is None
 
    def cantidad(self):
        return self.__tamano
 
    def apilar(self, paquete):
        self.__tope = Nodo(paquete, self.__tope)
        self.__tamano += 1
 
    def ver_tope(self): 
        if self.esta_vacia():
            raise ErrorPorteria("No hay entregas para deshacer")
        return self.__tope.dato
 
    def desapilar(self):
        if self.esta_vacia():
            raise ErrorPorteria("No hay entregas para deshacer")
        dato = self.__tope.dato
        self.__tope = self.__tope.siguiente
        self.__tamano -= 1
        return dato