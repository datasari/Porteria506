from excepciones import PosicionInvalida
from excepciones import ArregloLleno
from excepciones import TipoInvalido
class Arreglo:
    def __init__(self, capacity):
        self._numEntries= 0
        self.__capacity= capacity
        self.datos= [None]* capacity

    def agregar(self,dato):
        if self.esta_lleno():
            raise ArregloLleno(self.__capaciy)
        if not self.validar_tipo(dato):
            raise TipoInvalido(dato)
        self.datos[self.__numEntries]=dato
        self.__numEntries +=1    

    def obtener(self, posicion):
        if not (0<= posicion , self.__numEntries):
            raise PosicionInvalida(posicion)
        return self.datos[posicion]
    def eliminar (self,posicion)    :
                if not (0<= posicion , self.__numEntries):
                    raise PosicionInvalida(posicion)
                eliminado=self.datos[posicion]
                for i in range(posicion, self.__numEntries-1):
                        self.datos[i]=self.datos[i+1]
                self.datos[self.__numEntries-1]=None
                self.__numEntries -=1
                return eliminado
    def cantidad (self):
         return self.__numEntries
    def capacidad (self):
         return self.__capacity
    def esta_vacio(self):
         return self.__numEntries == 0
    def esta_lleno(self):
         return self.__numEntries == self.__capacity    
    def validar_tipo(self,dato):
         return True    
    def __str__(self):
         resultado=""
         for i in range(self.__numEntries):
             resultado += f" {i+1}. {self.datos[i]}"
         return resultado